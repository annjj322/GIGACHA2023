 #!/usr/bin/env python3
import json
import threading
import numpy as np
import rospy
from local_pkg.msg import Local
from math import hypot, sqrt
from time import sleep
import matplotlib.pyplot as plt
from shared.path import Path

'''
해야할 일
굳이 이 필터를 사용한 억지 당위성
input과 output에 필터를 적용 전/후
원본과 최종 비교

'''

class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        rospy.Subscriber('/local_msgs', Local, self.local_callback)

        # tmp
        self.global_path_tmp = Path()
        self.plot_flag =False


        self.mapname = parent.args.map
        self.period = 1.0 / rate
        print(self.mapname)
        self.ego = parent.shared.ego
        self.plan = parent.shared.plan
        self.global_path = parent.shared.global_path
        self.local_path = parent.shared.local_path
        self.perception = parent.shared.perception
        self.read_global_path()  # only one time
        self.hAcc = 100000
        self.x = 0
        self.y = 0
        self.index_finder()


        

    def local_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.hAcc = msg.hAcc
        self.ego.speed = msg.speeed
        self.ego.heading = msg.heading
        self.ego.orientaion = msg.orientation
        self.ego.dr_x = msg.dr_x
        self.ego.dr_y = msg.dr_y
        self.ego.roll = msg.roll
        self.ego.pitch = msg.pitch

        self.ego.x = msg.x
        self.ego.y = msg.y
        
    def read_global_path(self):
        
        with open(f"maps/{self.mapname}.json", 'r') as json_file:
            json_data = json.load(json_file)
            for n, (x, y, mission,_
                    ) in enumerate(json_data.values()):
                self.global_path.x.append(x)
                self.global_path.y.append(y)
                self.global_path.mission.append(mission)

        for i in range(len(self.global_path.x)):
            if i%2==0:
                self.global_path_tmp.x.append(self.global_path.x[i])
                self.global_path_tmp.y.append(self.global_path.y[i])

        data = np.array(self.curvedBaseVelocity(self.global_path_tmp, 100))
        
        # 곡률기반 속도에 필터 적용
        filtered_data = self.moving_average(data, 15)
        filtered_data2 = self.moving_average(filtered_data, 15)
        filtered_data3 = self.moving_average(filtered_data2, 15)

        result = filtered_data3
        print(len(result))
        
        for i in range(len(result)-1):
            self.ego.map_speed.append(result[i])
            self.ego.map_speed.append((result[i]+result[i+1])/2)
        self.ego.map_speed.append(0)

        print(len(self.ego.map_speed))
        print("yaho yaho")


        if self.plot_flag:
            plt.plot(data, "k", label="original data")
            plt.plot(result, "r", label="filtered data")
            plt.title('EXTRA BIG PJM')
            plt.legend()
            plt.grid()
            plt.show()

    def moving_average(self, data, window_size):
        # 이동 평균 계산을 위해 필요한 윈도우 크기보다 작은 경우 예외 처리
        if len(data) < window_size:
            raise ValueError("데이터 크기가 윈도우 크기보다 작습니다.")
        
        # 이동 평균 계산
        weights = np.repeat(1.0, window_size) / window_size
        ma = np.convolve(data, weights, 'valid')
        
        result = []
        for i in range(window_size//2):
            result.append(data[i])
        for val in ma:
            result.append(val)
        for i in range(window_size//2):
            result.append(data[i])

        return result
    
    def index_finder(self):
        min_dis = -1
        min_idx = 0
        step_size = 50
        # save_idx = self.ego.index                    # for not decreasing index
        save_idx = 0
        # for i in range(max(self.ego.index - step_size, 0), self.ego.index + step_size):
        for i in range(len(self.global_path.x)): 
            try:
                dis = hypot(
                    self.global_path.x[i] - self.ego.x, self.global_path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i
        self.ego.index = min_idx
        self.plan.mission_decision = self.global_path.mission[self.ego.index]    
    
    def local_index_finder(self):
        if len(self.local_path.x) != 0:
            min_dis = -1
            min_idx = 0
            step_size = 50
            # save_idx = self.ego.index                    # for not decreasing index
            save_idx = 0
            # for i in range(max(self.ego.index - step_size, 0), self.ego.index + step_size):
            for i in range(len(self.local_path.x)): 
                try:
                    dis = hypot(
                        self.local_path.x[i] - self.ego.x, self.local_path.y[i] - self.ego.y)
                except IndexError:
                    break
                if (min_dis > dis or min_dis == -1) and save_idx <= i:
                    min_dis = dis
                    min_idx = i
                    save_idx = i
            self.ego.local_index = min_idx
        else:
            self.ego.local_index = 0   
            # print("here!!", len(self.local_path.mission))
            # print("local_index", self.ego.local_index)
            # self.plan.mission_decision = self.local_path.mission[self.ego.local_index]       
            
    def dead_reckoning(self):
        if self.hAcc < 50 :
            self.ego.x = self.x
            self.ego.y = self.y
        else:
            self.ego.x = self.ego.dr_x
            self.ego.y = self.ego.dr_y

    def run(self):
        while True:
            self.index_finder()
            self.local_index_finder()
            self.dead_reckoning()
            sleep(self.period)

    def curvedBaseVelocity(self, global_path, point_num):
        car_max_speed = 20
        out_vel_plan = []
        r_list = []
        tmp = []

        for i in range(0,point_num):
            out_vel_plan.append(car_max_speed)
            r_list.append(0)

        for i in range(point_num, len(global_path.x) - point_num):
            x_list = []
            y_list = []
            for box in range(-point_num, point_num):
                x = global_path.x[i+box]
                y = global_path.y[i+box]
                x_list.append([-2*x, -2*y ,1])
                y_list.append((-x*x) - (y*y))

            #TODO: (6) 도로의 곡률 계산
            x_matrix = np.array(x_list)
            y_matrix = np.array(y_list)
            x_trans = x_matrix.T

            a_matrix = np.linalg.inv(x_trans.dot(x_matrix)).dot(x_trans).dot(y_matrix)
            
            a = a_matrix[0]
            b = a_matrix[1]
            c = a_matrix[2]
            r = sqrt(a*a+b*b-c)
            # r_list.append(r)
            tmp.append(r)

            #TODO: (7) 곡률 기반 속도 계획
            # road_friction = 0.4
            # v_max = sqrt(r*9.8)

            # if v_max > car_max_speed:
            #     v_max = car_max_speed
            
            # out_vel_plan.append(v_max)



############# 곡률 게산한 것에 필터 적용한 곳
        result = self.moving_average(np.array(tmp), 15)

        for r in result:
            # v_max = min(sqrt(r*9.8), car_max_speed)
            # out_vel_plan.append(v_max)
            v_max = sqrt(r*9.8)
            if v_max > car_max_speed:
                v_max = car_max_speed
            
            out_vel_plan.append(v_max)


###############
        if self.plot_flag:
            plt.plot(tmp, "k", label="original data")
            plt.plot(result, "r", label="filtered data")

            plt.grid()
            plt.legend()
            plt.show()
    
        for i in range(len(self.global_path.x) - point_num, len(self.global_path.x)-10):
            out_vel_plan.append(20)

        for i in range(len(self.global_path.x) - 10, len(self.global_path.x)):
            out_vel_plan.append(0)



        return out_vel_plan


    def change_speed(self, list, index, max):
        #보류
        left_flag = False
        right_flag = False

        for j in range(1, 7):
            if list[index-j] == max:
                left_flag = True
            if list[index+j] == max:
                right_flag = True

        if left_flag and right_flag:
            return True
        else:
            return False
