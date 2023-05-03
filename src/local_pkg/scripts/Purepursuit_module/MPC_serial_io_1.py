#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
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
import math

import MPC_XY_Frame as MPC

class Serial_IO:
    def __init__(self):

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
        self.velocity = []

        # rospy Rate
        self.rt = 20

    def run(self):
        rate = rospy.Rate(self.rt)
        
        ##################
        global_path_x, global_path_y = MPC.read_global_path()
        cx, cy, cyaw, ck, s = MPC.cs.calc_spline_course(
            global_path_x, global_path_y, ds = MPC.P.d_dist)
        # cx = global_path index x list
        # cy = global_path index y list
        # cyaw = global_path index yaw list
        # ck = global_path index curvature list

        sp = MPC.calc_speed_profile(cx, cy, cyaw, MPC.P.target_speed) # speed profile list
        
        ref_path = MPC.PATH (cx, cy, cyaw, ck) # reference global path
        
        node = MPC.Node(x=cx[0], y=cy[0], yaw=cyaw[0], v=0.0)
        # x, y, yaw, v at specific index of global_path
        # reset at first try

        time = 0.0
        x = [node.x] # list of node x
        y = [node.y] # list of node y
        yaw = [node.yaw] # list of node yaw
        v = [node.v] # list of node velocity
        t = [0.0] # list of node time
        d = [0.0] # list of node steer
        a = [0.0] # list of node acceleration

        delta_opt, a_opt = None, None
        a_exc, delta_exc = 0.0, 0.0

        while not rospy.is_shutdown():

            z_ref,ego_ind = \
                MPC.calc_ref_trajectory_in_T_step(node, ref_path, sp)
                #하는일 : 내 인덱스 찾아주고, 예측하고 싶은 갯수 만큼 ref_path에서 점 만들어줌
            #print(target_ind)
            z0 = [node.x, node.y, node.v, node.yaw]

            a_opt, delta_opt, x_opt, y_opt, yaw_opt, v_opt = \
                MPC.linear_mpc_control(z_ref, z0, a_opt, delta_opt)
            #predict_states_in_T_step함수 node.update해서 선형적 모델로 x,y,v,yaw
            #예측함 그래서 만든게 z_bar,, 최적화를 마친 T개의 x,y,v,yaw를 반환함(solve_linear_mpc)
            #
            # a_opt = a_old, delta_opt = delta_old
            # print("z0:", z0)
            # print("z_ref:", z_ref)
            if delta_opt is not None:
                delta_exc, a_exc = delta_opt[0], a_opt[0] # first index of list

            node.update(a_exc, delta_exc, 1.0)
            time += MPC.P.dt
            # delta_exc = np.rad2deg(delta_exc)
            print(delta_exc)
            x.append(node.x)
            y.append(node.y)
            yaw.append(node.yaw)
            v.append(node.v)
            t.append(time)
            d.append(delta_exc)
            a.append(a_exc)
            
            dist = math.hypot(node.x - cx[-1], node.y - cy[-1])
            # distance of ego to destination
            
            if dist < MPC.P.dist_stop and \
                    abs(node.v) < MPC.P.speed_stop:
                break
            # stop to folow the global path
            if abs((delta_exc))<0.5:
                delta_exc = 0
            dy = (node.yaw - yaw[-2]) / (node.v * MPC.P.dt)
            steer = MPC.pi_2_pi(-math.atan(MPC.P.WB * dy))
            delta_exc = np.degrees(delta_exc)
            # print(np.degrees(-steer))
            self.setValue(node.v, delta_exc, 0)
            # if self.ego_info.speeed == 0 : # -> must modify
            #     plt.show()
            #     plt.plot(x_opt, y_opt, color='darkviolet', marker='*')
            #     plt.plot(cx, cy, color='gray')
            #     plt.plot(self.curPosition_x, self.curPosition_y, '-b')
            #     plt.plot(cx[target_ind], cy[target_ind])
            #     plt.axis("equal")
            #     plt.title("Linear MPC, " + "v = " + str(round(node.v * 3.6, 2)))
            #     plt.pause(0.001)
            self.save_position()
            # if time > 1000.0:
            #     plt.show()
            #     plt.plot(global_path_x,global_path_y,'k-',label='global_path')
            #     plt.plot(self.curPosition_x,self.curPosition_y,'ro',label='present_route',ms=2)
            #     plt.grid()
            #     # plt.legend(loc="lower right")
            #     plt.title("Global_path vs Car_trajectory")
            #     plt.xlabel('x')
            #     plt.ylabel('y')
                
            self.serialWrite()
            ########################### print values ##############################
            # print("current_x: ", round(node.x,4), "real_x: ", round(self.ego_info.x,4))
            # print("current_y: ", round(node.y,4), "real_y: ", round(self.ego_info.y,4))
            # print("current_yaw: ", round(node.yaw,4), "real_y: ", round(self.ego_info.heading,4))
            # print("steer: ", self.serial_msg.steer)

            print("difference x: ", node.x - self.ego_info.x)
            print("difference y: ", node.y - self.ego_info.y)
            # print("time: ", time)
            # print("delta_opt: ", delta_opt)
            # print("current_v: ", node.v)
            # print("current_yaw: ", node.yaw, "\n")
            # print("current_steer: ", self.control_input.steer)
            # print("x: ", self.ego_info.x)
            # print("y: ", self.ego_info.y)
            # print("v: ", self.ego_info.speeed)
            # print("yaw: ", self.ego_info.heading, "\n")
            ########################### print values ##############################
            # rate.sleep()
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

        self.control_input.speed = max(0, min(self.control_input.speed, 27))

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
