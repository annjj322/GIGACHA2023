#!/usr/bin/env python3
from sig_int_handler import Activate_Signal_Interrupt_Handler
import serial
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from local_pkg.msg import Local
import threading
import struct
import rospy
from math import sqrt, atan2, sin, atan, cos, sqrt
from numpy import degrees, radians, hypot, array, argmin, arange
import json
import matplotlib.pyplot as plt
from geometry_msgs.msg import PoseArray
import numpy as np
import time


class Serial_IO:
    def __init__(self):
        self.k = 0.55
        # self.k = 0.15
        self.WB = 1.04 # wheel base

        # Global Path
        self.global_path_x = []
        self.global_path_y = []

        # Ego information      
        self.curPosition_x = []
        self.curPosition_y = []
        self.velocity = []
        self.gps_to_Lidar = 1.3

        # Obstacle information
        self.obj_x = None
        self.obj_y = None
        self.objPosition_x = []
        self.objPosition_y = []

        # Reading Global Path
        self.read_global_path()

        # self.stop_index = [800, 1200, 2500, 4450]
        self.stop_index = len(self.global_path_x)
       
        # Serial Connect
        self.ser = serial.Serial("/dev/erp42", 115200) # Real World        
        # self.ser = serial.Serial("/dev/ttyUSB0", 115200) # Simulation


        # ROS Publish
        rospy.init_node("Serial_IO", anonymous=False)
        self.serial_pub = rospy.Publisher("/serial", Serial_Info, queue_size=1)
       
        # Messages/Data
        self.serial_msg = Serial_Info()  # Message o publish
        self.alive = 0

        # Subscribing Ego information
        rospy.Subscriber("/local_msgs", Local, self.localcallback)

        # Subscribing Obstacle information
        rospy.Subscriber("/pcd", PoseArray, self.obstaclecallback)

        # Declaration
        self.ego_info = Local()
        self.control_input = Control_Info()

        

        # self.obstacle_info = PoseArray()
        self.obstacle_info_x = 0
        self.obstacle_info_y = 0

        # Pure Pursuit coefficient
        self.lookahead_default = 10
        # self.lookahead_default = 4
        self.ego_index = None

        # Stop coefficient
        self.stop_index_coefficient = 10
        self.brake_coefficient = 6

        # Serial Read Thread
        th_serialRead = threading.Thread(target=self.serialRead)
        th_serialRead.daemon = True
        th_serialRead.start()

        # rospy Rate
        self.rt = 20
        
        # Value reset to 0 for start
        self.setValue(0,0,0)

    def run(self):
        '''
        !!!!!!!!!!!!!!!!!!!!!!!! 경고 !!!!!!!!!!!!!!!!!!!!!!!
        speed_limit 20으로 두면 사고남. morai로도 ERP 속도는 20이 안나오니까 20 금지.
        
        이봄이 할 수 있는 것 

            다른 함수는 필요없고 speed_limit 만 바꾸면 됨.
            여기서 self.setValue 처음 값이 속도, 두번째 값이 조향각, 세번째 값이 브레이크임.
            메인 루프에서 ERP 속도를 받아오는데 이게 정해준 값보다 크면 브레이크를 밟도록 해두었음
        
        매번 키기 귀찮을 이와 봄을 위해 준비한 기능
            1. 중립기어인 상태로 자율주행모드를 킨다.
            2. 테스트가 끝나면 자율주행모드를 껐다 킨다.
            3. 반복한다.

        어차피 한번씩하고 데이터 저장할 생각이라면 그냥 무시하셈
        '''
        rate = rospy.Rate(self.rt)

        passing = False

        while not rospy.is_shutdown():
            speed_limit = 19 # HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if speed_limit >= 20 :
                print('이봄 경고. 정신 차릴 것.')
                break
            else:
                if self.serial_msg.speed >= speed_limit or passing == True: 
                    self.setValue(0,self.pure_pursuit(), 100)
                    passing = True
                else:    
                    self.setValue(10, self.pure_pursuit(), 0)

            if self.serial_msg.gear == 1:
                passing = False

            self.serialWrite()
            rate.sleep()

    def serialRead(self):
        print("Serial_IO: Serial reading thread successfully started")

        while True:
            
            print(f"Serial_IO: Reading serial {self.alive}")

            packet = self.ser.read_until(b'\x0d\x0a')
            if len(packet) == 18:
                header = packet[0:3].decode()

                if header == "STX":
                    (self.serial_msg.auto_manual,
                    self.serial_msg.emergency_stop,
                    self.serial_msg.gear) \
                    = struct.unpack("BBB", packet[3:6])
                    
                    tmp1, tmp2 = struct.unpack("2h", packet[6:10])
                    self.serial_msg.speed = tmp1 / 10  # km/h

                    self.serial_msg.steer = tmp2 / 71  # degree


                    self.alive = struct.unpack("B", packet[15:16])[0]

                    self.serial_pub.publish(self.serial_msg)

    def serialWrite(self):
        if self.control_input.speed > 20:
            self.control_input.speed = 20

        self.control_input.speed = max(0, min(self.control_input.speed, 20))

        if self.control_input.brake > 200:
            self.control_input.brake = 200

        result = struct.pack(  #
            ">BBBBBBHhBBBB",
            0x53,
            0x54,
            0x58,
            1, #always auto
            self.control_input.emergency_stop,
            self.control_input.gear,
            int(self.control_input.speed * 10),
            int(self.control_input.steer * 71),
            int(self.control_input.brake),
            self.alive,
            0x0D,
            0x0A
        )
        self.ser.write(result)

    def localcallback(self, msg):
        self.ego_info.x = msg.x
        self.ego_info.y = msg.y
        self.ego_info.heading = msg.heading
        self.ego_info.speeed = msg.speeed

        

    def read_global_path(self):
        with open(f"/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/kcity_simul/semi_map.json", 'r') as json_file:
        # with open(f"/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/kcity_simul/semi_map.json", 'r') as json_file:
        
            json_data = json.load(json_file)
            for _, (x, y, _, _) in enumerate(json_data.values()):
                self.global_path_x.append(x)
                self.global_path_y.append(y)

    def calc_distance(self, point_x, point_y):
        dx = self.ego_info.x - point_x
        dy = self.ego_info.y - point_y
        d = hypot(dx,dy)
        return d

    def obstaclecallback(self,msg):
        if msg.poses[0].orientation.z == 100:
            pass
        else:
            self.obstacle_info_x = msg.poses[0].orientation.x # relative coordinate obstacle x
            self.obstacle_info_y = msg.poses[0].orientation.y # relative coordinate obstacle y
            self.find_obstacle()

            if self.stop_index is not None:
            # self.stop_index = self.target_index()
                if abs(self.stop_index - self.ego_index) >= 50: # 5m -> No Update. Fixxed Value.            
                    self.stop_index = self.target_index()   
                    # self.stop_index = 497

    def distance(self, x, y):
        return sqrt(x**2+y**2)

    def search_ego_index(self):
        d = []
        self.dx = []
        self.dy = []
        for i in range(len(self.global_path_x)):
            self.dx.append(self.ego_info.x - self.global_path_x[i])
            self.dy.append(self.ego_info.y - self.global_path_y[i])
        
        for i in range(len(self.dx)):
            d.append(self.distance(self.dx[i], self.dy[i]))
        
        new_d = array(d)
        ind = argmin(new_d)
        self.dx = []
        self.dy = []
        
        self.ego_index = ind

        Lf = self.k * self.ego_info.speeed + self.lookahead_default  # update look ahead distance

        # search look ahead target point index
        while Lf > self.calc_distance(self.global_path_x[ind], self.global_path_y[ind]):
            if (ind + 1) >= len(self.global_path_x):
                break  # not exceed goal
            ind += 1

        return ind, Lf

    def pure_pursuit(self):
        ind,Lf=self.search_ego_index()
        lookahead = min(Lf, 6)
        target_index = ind 
        
        target_x, target_y = self.global_path_x[target_index], self.global_path_y[target_index]
        tmp = degrees(atan2(target_y - self.ego_info.y,
                            target_x - self.ego_info.x)) % 360

        alpha = self.ego_info.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)
        if degrees(angle) < 0.5 and degrees(angle) > -0.5:
            angle = 0
        tmp_steer = degrees(angle) 
        if abs(tmp_steer) > 5: 
            tmp_steer *= 0.8

        steer = max(min(tmp_steer, 27.0), -27.0) 
        return steer



    def setValue(self, speed, steer, brake):
        self.control_input.speed = speed
        self.control_input.steer = steer
        self.control_input.brake = brake



if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    erp = Serial_IO().run()
