from math import sqrt, hypot
from time import time, sleep
from math import cos, sin, pi, sqrt
from local_pkg.msg import Control_Info
import rospy
from . parking_diagonal_LJY import *

class Mission():
    def __init__(self, sh, eg, pc, pl):

        self.perception = pc
        self.shared = sh
        self.ego = eg
        self.plan = pl
        self.parking = self.shared.park

        self.global_path = self.shared.global_path
        self.time_checker = False
        
        self.obstacle_checker = False
        self.emergency_check = False
        self.obstacle_stop = False

        self.now = 0

        self.parking_path_maker = False
        self.parking_forward_start = False
        self.parking_backward_start = False
        self.parking_switch = False
        self.parking_create = False
        self.force_switch = False
        self.inflection_switch = False
        
        self.first_stop = False
        self.second_stop = False
        self.third_stop = False
        self.fourth_stop = False
        self.backward_tra_create = False
        self.backward_tra_create1 = False
        self.backward_tra_create2 = False
        self.forward_tra_create = False
        self.forward_reverse_tra_create = False
        self.parallel_flag=False
        self.exit_flag=False
        self.hy_test=False
        self.parking_turning=False
        self.global_path_storage_full = False
        self.global_path_storage_x = []
        self.global_path_storage_y = []

        self.speed = 10

    def range(self, a, b):
        return (a-b) <= self.ego.index <= a

    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed

    def go(self):
        self.ego.target_estop = 0x00
        self.ego.target_gear = 0
        self.ego.target_speed = self.speed
        self.plan.behavior_decision = "driving"


######################################################################################################################################
    def Parking_KCity_diagonal_LJY(self):
        if (self.parking_create == False):
            if (700 <= self.ego.index <= 720) and self.first_stop == False: # K-City
                if self.global_path_storage_full == False:
                    self.global_path_storage_x = self.global_path.x
                    self.global_path_storage_y = self.global_path.y
                    self.global_path_storage_full = True
                elif self.global_path_storage_full == True:
                    self.plan.behavior_decision = "stop"
                    self.target_control(100, 0)
                    sleep(3)
                    self.first_stop = True

            if (self.first_stop == True) and (self.second_stop == False):
                if self.backward_tra_create == False:
                    self.plan.behavior_decision = "backward_trajectory_Create"
                    self.backward_tra_create = True
                elif self.backward_tra_create == True:
                    self.plan.behavior_decision = "parkingBackwardOn"
                    # self.plan.behavior_decision = "driving"
                    self.ego.target_gear = 2
                    self.parking.on = "on"
                    self.target_control(0, 5)
                    print("len: ", len(self.global_path.x))
                    print("ego_ind: ", self.ego.index)
                    if len(self.global_path.x) - 20 <= self.ego.index <= len(self.global_path.x):
                        self.target_control(100, 0)
                        sleep(3) 
                        self.second_stop = True # 경로와 직선 사이 교점 근처에 정차
                        self.global_path.x = self.global_path_storage_x # 다시 원래 경로
                        self.global_path.y = self.global_path_storage_y


            if (self.second_stop == True) and (self.third_stop == False):
                if self.forward_tra_create == False:
                    self.plan.behavior_decision = "forward_trajectory_Create"
                    self.forward_tra_create = True
                elif self.forward_tra_create == True:
                    self.plan.behavior_decision = "parkingForwardOn"
                    # self.plan.behavior_decision = "driving"
                    self.ego.target_gear = 0
                    self.parking.on = "off"
                    self.target_control(0, 3)
                    print("len: ", len(self.global_path.x))
                    print("ego_ind: ", self.ego.index)
                    if len(self.global_path.x) - 10 <= self.ego.index <= len(self.global_path.x):
                        self.target_control(100, 0)
                        sleep(3) 
                        self.third_stop = True # 사선 주차 성공

            if (self.third_stop == True) and (self.fourth_stop == False):
                if self.forward_reverse_tra_create == False:
                    self.plan.behavior_decision = "forward_reverse_trajectory_Create"
                    self.forward_reverse_tra_create = True
                elif self.forward_reverse_tra_create == True:
                    # self.plan.behavior_decision = "parkingBackwardOn"
                    self.plan.behavior_decision = "parkingForwardOn"
                    self.ego.target_gear = 2
                    self.parking.on = "on"
                    self.target_control(0, 3)
                    print("len: ", len(self.global_path.x))
                    print("ego_ind: ", self.ego.index)
                    if len(self.global_path.x) - 20 <= self.ego.index <= len(self.global_path.x):
                        self.target_control(100, 0)
                        sleep(3) 
                        self.fourth_stop = True # 경로와 직선 사이 교점 근처에 정차
                        self.parking_create = True # 주차미션 종료
            else: # 처음에 주행
                self.plan.state = "go"
        else: # 원래대로 주행
            self.global_path.x = self.global_path_storage_x # 다시 원래 경로
            self.global_path.y = self.global_path_storage_y
            self.parking.on = "off"
            self.shared.plan.behavior_decision == "driving"
            self.plan.state = "go"
            self.ego.target_gear = 0
            self.target_control(0, 20)
                    

#######################################################################################################################################
    def Parking_KCity_parallel_hy(self):
            if (self.parking_create == False):
                if (3580 <= self.ego.index <= 3650) and self.first_stop == False: # K-City
                    if self.global_path_storage_full == False:
                        self.global_path_storage_x = self.global_path.x
                        self.global_path_storage_y = self.global_path.y
                        self.global_path_storage_full = True
                    elif self.global_path_storage_full == True:
                        self.plan.behavior_decision = "stop"
                        self.target_control(100, 0)
                        sleep(2) #일단 주차 구간에 들어왔으니 멈출게?
                        self.first_stop = True

                if (self.first_stop == True) and (self.second_stop == False):
                    if self.forward_tra_create == False:
                        self.plan.behavior_decision = "forward_trajectory_Create"
                        self.forward_tra_create = True #전진 경로 만들었다. 
                    elif self.forward_tra_create == True: #전진 경로 만들었으니까 이제 할게?
                        self.plan.behavior_decision = "parkingForwardOn"
                        self.ego.target_gear = 0
                        self.parking.on = "hy"
                        self.target_control(0, 5)
                        # print("len: ", len(self.global_path.x))
                        # print("ego_ind: ", self.ego.index)
                        print('성공했나???????')
                        #d=self.cal_cal(self.global_path.x[-1],self.global_path.y[-1])
                        if len(self.global_path.x) - 10 <= self.ego.index <= len(self.global_path.x):
                            self.target_control(100, 0) #전지해야할 곳 도착쓰
                            sleep(3) 
                            print('/////////////////////////////')
                            self.second_stop = True 
                            

                if (self.second_stop == True) and (self.third_stop == False):
                    if self.backward_tra_create1 == False:
                        self.plan.behavior_decision = "backward_trajectory_Create"
                        self.backward_tra_create1 = True
                        print('경로 생성 완료!!!')
                    elif self.backward_tra_create1 == True:
                        self.plan.behavior_decision = "parkingBackwardOn"
                        self.ego.target_gear = 2
                        # self.ego.target_steer = 27
                        self.parking.on = "hy"
                        
                        print('가나연???????????')
                        self.target_control(0, 5)
                        print("len: ", len(self.global_path.x))
                        print("ego_ind: ", self.ego.index)
                        #d1=self.cal_cal(self.self.global_path.x[-1],self.global_path.y[-1])
                        if len(self.global_path.x) - 2 <= self.ego.index <= len(self.global_path.x):
                            self.target_control(100,0)
                            sleep(2)
                            self.third_stop= True
                if (self.third_stop ==True) and (self.fourth_stop ==False) :
                        if self.backward_tra_create2==False:    
                            self.plan.behavior_decision="mamuri"
                            self.backward_tra_create2=True
                        elif self.backward_tra_create2:
                            self.plan.behavior_decision = "parkingFowardOn"
                            self.ego.target_gear = 0
                            self.parking.on = "hy"
                            self.target_control(0, 3)
                            if len(self.global_path.x) - 40 <= self.ego.index <= len(self.global_path.x):                           
                                self.target_control(100,0)
                                sleep(2)
                                self.fourth_stop=True
                                # self.parking_create=True
                if (self.fourth_stop==True) and (self.parallel_flag==False):
                    if self.exit_flag==False:
                        self.plan.behavior_decision="exit"
                        self.exit_flag=True
                    elif (self.exit_flag==True) and (self.parking_turning==False):
                        self.plan.behavior_decision="parkingBackwardOn"
                        self.ego.target_gear=2
                        self.target_control(0,1)
                       
                        if len(self.global_path.x) - 45 <= self.ego.index <= len(self.global_path.x):                           
                                self.target_control(100,0)
                                sleep(2)
                                self.parking_turning=True
                                print('여기기기기기기ㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣ?')
                                self.plan.behavior_decision="backward_trajectory_Create"
                                
                    else:
                        self.plan.behavior_decision="parkingFowardOn"
                        print('d진짜ㅏ찐 마짐가가가가가가가가')
                        self.ego.target_gear=0
                        self.target_control(0,1)
                        if len(self.global_path.x) - 15 <= self.ego.index <= len(self.global_path.x):                           
                                self.target_control(100,0)
                                sleep(2)
                                self.parking_create=True
                                self.parking_turuning=False
                                self.parallel_flag=True
                                
                else:
                    self.plan.state = "go"
            else: # 원래대로 주행
                self.ego.index=3000
                self.global_path.x = self.global_path_storage_x # 다시 원래 경로
                self.global_path.y = self.global_path_storage_y
                self.parking.on = "off"
                self.shared.plan.behavior_decision == "driving"
                self.plan.state = "go"
                self.ego.target_gear = 0
                self.target_control(0, 20)
                
                                    
   ##################################################################################
    #######################################################################################################################################
    def Parking_KCity_parallel_hy_test(self):
            if (self.parking_create == False):
                if (3580 <= self.ego.index <= 3650) and self.first_stop == False: # K-City
                    if self.global_path_storage_full == False:
                        self.global_path_storage_x = self.global_path.x
                        self.global_path_storage_y = self.global_path.y
                        self.global_path_storage_full = True
                    elif self.global_path_storage_full == True:
                        # self.plan.behavior_decision = "stop"
                        self.target_control(100, 0)
                        sleep(1) #일단 주차 구간에 들어왔으니 멈춤.
                        self.first_stop = True

                if (self.first_stop == True) and (self.second_stop == False):
                    if self.forward_tra_create == False:
                        self.plan.behavior_decision = "forward_trajectory_Create"
                        self.forward_tra_create = True #전진 경로 만들었다. 
                    elif self.forward_tra_create == True: #전진 경로 만들었으니까 이제 할게?
                        self.plan.behavior_decision = "parkingForwardOn"
                        self.ego.target_gear = 0
                        self.parking.on = "hy"
                        self.target_control(0, 5)
                        if len(self.global_path.x) - 10 <= self.ego.index <= len(self.global_path.x):
                            self.target_control(100, 0) #전지해야할 곳 도착쓰
                            sleep(3) 
                            print('/////////////////////////////')
                            self.second_stop = True 
                            

                if (self.second_stop == True) and (self.third_stop == False):
                    if self.backward_tra_create1 == False:
                        self.plan.behavior_decision = "backward_trajectory_Create"
                        self.backward_tra_create1 = True
                        print('경로 생성 완료!!!')
                    elif self.backward_tra_create1 == True and (self.hy_test ==False):
                        self.plan.behavior_decision = "parkingBackwardOn"
                        self.ego.target_gear = 2
                        self.ego.target_steer = 27
                        self.parking.on = "forced"
                        
                        print('가나연???????????')
                        self.target_control(0, 3)
                        print("len: ", len(self.global_path.x))
                        print("ego_ind: ", self.ego.index)
                        #d1=self.cal_cal(self.self.global_path.x[-1],self.global_path.y[-1])
                        if 40 <= self.ego.index <=45:
                            self.hy_test=True
                if (self.second_stop == True) and (self.third_stop == False) and (self.hy_test==True):
                        self.plan.behavior_decision = "parkingBackwardOn"
                        self.ego.target_gear = 2
                        self.ego.target_steer = -27
                        self.parking.on = "forced"
                        
                        print('가나연???????????')
                        self.target_control(0, 3)
                        if len(self.global_path.x) - 10 <= self.ego.index <= len(self.global_path.x):
                            self.target_control(100,0)
                            sleep(2)
                            self.third_stop= True
                if (self.third_stop ==True) and (self.fourth_stop ==False) :
                        if self.backward_tra_create2==False:    
                            self.plan.behavior_decision="mamuri"
                            self.backward_tra_create2=True
                        elif self.backward_tra_create2:
                            self.plan.behavior_decision = "parkingFowardOn"
                            self.ego.target_gear = 0
                            self.parking.on = "hy"
                            self.target_control(0, 3)
                            if len(self.global_path.x) - 40 <= self.ego.index <= len(self.global_path.x):                           
                                self.target_control(100,0)
                                sleep(2)
                                self.fourth_stop=True
                                # self.parking_create=True
                if (self.fourth_stop==True) and (self.parallel_flag==False):
                    if self.exit_flag==False:
                        self.plan.behavior_decision="exit"
                        self.exit_flag=True
                    elif (self.exit_flag==True) and (self.parking_turning==False):
                        self.plan.behavior_decision="parkingBackwardOn"
                        self.ego.target_gear=2
                        self.target_control(0,3)
                       
                        if len(self.global_path.x) - 40 <= self.ego.index <= len(self.global_path.x):                           
                                self.target_control(100,0)
                                sleep(2)
                                self.parking_turning=True
                                print('여기기기기기기ㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣ?')
                                self.plan.behavior_decision="backward_trajectory_Create"
                                
                    else:
                        self.plan.behavior_decision="parkingFowardOn"
                        print('d진짜ㅏ찐 마짐가가가가가가가가')
                        self.ego.target_gear=0
                        self.target_control(0,3)
                        if len(self.global_path.x) - 15 <= self.ego.index <= len(self.global_path.x):                           
                                self.target_control(100,0)
                                sleep(2)
                                self.parking_create=True
                                self.parking_turuning=False
                                self.parallel_flag=True
                                
                else:
                    self.plan.state = "go"
            else: # 원래대로 주행
                # self.ego.index=3000
                self.global_path.x = self.global_path_storage_x # 다시 원래 경로
                self.global_path.y = self.global_path_storage_y
                self.parking.on = "off"
                self.shared.plan.behavior_decision == "driving"
                self.plan.state = "go"
                self.ego.target_gear = 0
                self.target_control(0, 20)
                
                                    
   ##################################################################################
    def static_obstacle(self):
        self.plan.behavior_decision = "static_obstacle_avoidance"
        index = len(self.perception.objx)
        
        if (self.range(2175,50)) and self.obstacle_stop == False:
            self.target_control(100,0)
            sleep(3)
            self.target_control(0,10)
            self.obstacle_stop = True

        if (len(self.perception.objx) > 0):
            self.obs_dis = 15.5
            for i in range(0, index):
                self.dis = sqrt(
                    (self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
                self.obs_dis = min(self.obs_dis, self.dis)
                print(len(self.perception.objx), " ", self.obs_dis)

            if self.obs_dis <= 10:
                self.target_control(0, 5)
                self.obstacle_checker = True
                self.time_checker = False
                
        elif self.obstacle_checker == True:
            if self.time_checker == False:
                self.cur_t = time()
                self.time_checker = True
            if time() - self.cur_t < 3:
                self.target_control(0, 5)
            else:
                self.target_control(0, 7)
            
        else:
            self.target_control(0, 7)

    def turn_left(self):
        if self.perception.tleft == 1 or self.perception.tgreen == 1:
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
        else:
            if self.range(1610, 85):
                self.plan.behavior_decision = "stop"
                self.target_control(100, 0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)


    def convert_lidar(self):
        theta = (self.ego.heading) * pi / 180
        size = 0
        objx = []
        objy = []
        self.perception.tmp_lidar_lock.acquire()
        size = len(self.perception.tmp_objx)
        if(size != 0):
            for i in range(size):
                objx.append(self.perception.tmp_objx[i] * cos(theta) + self.perception.tmp_objy[i] * -sin(theta) + self.ego.x)
                objy.append(self.perception.tmp_objx[i] * sin(theta) + self.perception.tmp_objy[i] * cos(theta) + self.ego.y)
    
        self.perception.lidar_lock.acquire()   
        self.perception.objy = []
        self.perception.objx = []
        self.perception.objx = objx
        self.perception.objy = objy
        self.perception.objw = self.perception.tmp_objw
        self.perception.objh = self.perception.tmp_objh
        self.perception.lidar_lock.release()
        self.perception.tmp_lidar_lock.release()
    