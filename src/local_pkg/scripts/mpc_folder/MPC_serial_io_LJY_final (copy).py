#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sig_int_handler import Activate_Signal_Interrupt_Handler
import serial
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from local_pkg.msg import Local
# from local_pkg.msg import Path as customPath
# from local_pkg.msg import Perception
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
import math

import MPC_XY_Frame_LJY_modify2 as MPC

class Serial_IO:
    def __init__(self):
        self.k = 0.55
        # self.k = 0.15
        self.WB = 1.04 # wheel base

        # Global Path
        self.global_path_x = []
        self.global_path_y = []

        # Serial Connect
        # self.ser = serial.Serial("/dev/erp42", 115200) # Real World        
        self.ser = serial.Serial("/dev/ttyUSB0", 115200) # Simulation

        # ROS Publish
        rospy.init_node("Serial_IO", anonymous=False)
        self.serial_pub = rospy.Publisher("/serial", Serial_Info, queue_size=1)
       

        # Subscribing Ego information
        rospy.Subscriber("/local_msgs", Local, self.localcallback)

        #Subscribe Control Info from Controller
        rospy.Subscriber("/controller", Control_Info, self.controlCallback)
        self.control_input = Control_Info()

        # Messages/Data
        self.serial_msg = Serial_Info()  # Message o publish
        self.alive = 0

        # Declaration
        self.ego_info = Local()

        # Serial Read Thread
        th_serialRead = threading.Thread(target=self.serialRead)
        th_serialRead.daemon = True
        th_serialRead.start()

        # Ego information      
        self.curPosition_x = []
        self.curPosition_y = []
        # error
        self.error = []
        self.abs_error = []

        # # rviz
        # self.global_path_pub = rospy.Publisher('/global_path', customPath, queue_size = 1)
        # self.trajectory_pub = rospy.Publisher('/trajectory', customPath, queue_size = 1)

        # rospy Rate
        self.rt = 20

        self.ind_old = 0
        # for purepursuit
        self.lookahead_default = 5

    def run(self):
        rate = rospy.Rate(self.rt)
        
        ##################
        global_path_x, global_path_y = MPC.read_global_path()
        cx, cy, cyaw, ck, s = MPC.cs.calc_spline_course(global_path_x, global_path_y, ds = MPC.P.d_dist)

        sp = MPC.calc_speed_profile(cx, cy, cyaw, MPC.P.target_speed) # speed profile
        
        ref_path = MPC.PATH(cx, cy, cyaw, ck)
        
        node = MPC.Node(x=cx[0], y=cy[0], yaw=cyaw[0], v=0.0)

        time = 0.0
        x = [node.x]
        y = [node.y]
        yaw = [node.yaw]
        v = [node.v]
        t = []

        plotx, ploty, cyaw, ck, s = MPC.cs.calc_spline_course(cx, cy, ds = MPC.P.d_dist)

        while not rospy.is_shutdown():
            
            ###################################################################3 
            node.x = self.ego_info.x
            node.y = self.ego_info.y
            node.yaw = self.ego_info.heading
            node.v = self.ego_info.speeed

            x.append(node.x)
            y.append(node.y)
            yaw.append(node.yaw)
            v.append(node.v)

            t.append(time)
            time += 1/self.rt

            z_ref, ego_ind = MPC.calc_ref_trajectory_in_T_step(node, ref_path, sp) # 내 인덱스에서 미래 reference state

            steer_list = MPC.mpc_pure_pursuit(node, ego_ind, cx, cy) # 내 위치에서 뽑아낸 미래 예측 steer들

            z_bar = MPC.mpc_predict_next_state(z_ref, node.x, node.y, node.yaw, node.v, v[-1], steer_list, direct = 1) # 미래 예측된 state # 위에서 뽑은 걸 기반으로 뽑아낸 예측 state

            selected_index = MPC.mpc_cost_function_LJY(z_ref, z_bar, steer_list) # z_ref와 z_bar을 기반으로 해서 다음 state index 정하기
            
            node.update(10, steer_list[selected_index], 1.0)

            self.curPosition_x.append(self.ego_info.x)
            self.curPosition_y.append(self.ego_info.y)
            self.abs_error.append(math.sqrt((plotx[ego_ind]-self.ego_info.x)**2 + (ploty[ego_ind]-self.ego_info.y)**2))
            #####################################################################

            # Graph Plot
            if 4000 < ego_ind < 4320:
                mean = sum(self.abs_error) / len(self.abs_error)
                print(mean)

                plt.show()
                plt.figure(1)
                # plt.plot(node.x, node.y, color='darkviolet', marker='*')
                plt.plot(cx, cy, color='gray')
                plt.plot(self.curPosition_x, self.curPosition_y, linewidth=3.0)
                # plt.plot(z_ref[0], cy[target_ind])
                plt.axis("equal")
                plt.title("Linear MPC, " + "v = " + str(round(node.v * 3.6, 2)))
                plt.pause(0.001)

                plt.figure(2)
                # plt.ylim(0,5)
                plt.plot(t, self.abs_error)
                # plt.plot(t, , color = 'red')
                plt.title("Position Error")
                plt.grid()
                plt.pause(0.001)
                
            self.setValue(z_ref[3, selected_index], steer_list[selected_index], 0)
            
            self.serialWrite()
            ########################### print values ##############################

            print("                  x         y        yaw       v")
            for i in range(MPC.P.T):
                print("Predict {:02d}: ".format(i+1),end='   ',)
                print('{:.4f}'.format(z_ref[0,i]),end='   ',)
                print('{:.4f}'.format(z_ref[1,i]),end='   ',)
                print('{:.4f}'.format(z_ref[2,i]),end='   ',)
                print('{:.4f}'.format(z_ref[3,i]))
            print("selected future x: ", z_ref[0, selected_index])
            print("selected future y: ", z_ref[1, selected_index])
            print("selected future yaw: ", z_ref[2, selected_index])
            print("selected future v: ", z_ref[3, selected_index])
            print("current index: ", ego_ind)

            rate.sleep()

    def serialRead(self):
        print("Serial_IO: Serial reading thread successfully started")

        while True:
            
            # print(f"Serial_IO: Reading serial {self.alive}")

            packet = self.ser.read_until(b'\x0d\x0a')
            # print(len(packet))
            if len(packet) == 18:
                header = packet[0:3].decode()

                if header == "STX":
                    #auto_manual, e-stop, gear
                    (self.serial_msg.auto_manual,
                    self.serial_msg.emergency_stop,
                    self.serial_msg.gear) \
                    = struct.unpack("BBB", packet[3:6])
                    
                    #speed, steer
                    tmp1, tmp2 = struct.unpack("2h", packet[6:10])
                    self.serial_msg.speed = tmp1 / 10  # km/h

                    self.serial_msg.steer = tmp2 / 71  # degree

                    self.alive = struct.unpack("B", packet[15:16])[0]

                    self.serial_pub.publish(self.serial_msg)

    def serialWrite(self):
        #Min/Max Limit
        if self.control_input.speed > 20:
            self.control_input.speed = 20

        self.control_input.speed = max(0, min(self.control_input.speed, 20))

        if self.control_input.brake > 33:
            self.control_input.brake = 33

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

    def controlCallback(self, msg):
        self.control_input = msg

    def save_position(self):
        self.curPosition_x.append(self.ego_info.x)
        self.curPosition_y.append(self.ego_info.y)

    
    def setValue(self, speed, steer, brake):
        self.control_input.speed = speed
        self.control_input.steer = steer
        self.control_input.brake = brake


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    erp = Serial_IO().run()
