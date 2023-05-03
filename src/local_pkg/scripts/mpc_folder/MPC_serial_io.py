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
        self.global_path_x, self.global_path_y = MPC.read_global_path()

        cx, cy, cyaw, ck, s = MPC.cs.calc_spline_course(
            self.global_path_x, self.global_path_y, ds = MPC.P.d_dist)
      
        sp = MPC.calc_speed_profile(cx, cy, cyaw, MPC.P.target_speed) # speed profile list
        
        ref_path = MPC.PATH (cx, cy, cyaw, ck) # reference global path
        
        node = MPC.Node(x=0.0, y=0.0, yaw=0.0, v=0.0)
        # x, y, yaw, v at specific index of global_path
        # reset at first try
        
        time = 0.0

        delta_opt, a_opt = None, None
        a_exc, delta_exc = 0.0, 0.0
        

        while not rospy.is_shutdown():

            node.x = self.ego_info.x
            node.y = self.ego_info.y
            node.yaw = self.ego_info.heading
            node.v = self.ego_info.speeed
            
            z_ref, ego_ind, target_ind= \
                MPC.calc_ref_trajectory_in_T_step(node, ref_path, sp)
            # print('z_ref')
            # print(z_ref[0,:])
            # print(z_ref[1,:])
            # print(z_ref[2,:])
            # print(z_ref[3,:])
            # print('ego')
            # print(node.yaw)
            z0 = [node.x, node.y, node.v, node.yaw]

            a_opt, delta_opt, x_opt, y_opt, yaw_opt, v_opt = \
                MPC.linear_mpc_control(z_ref, z0, a_opt, delta_opt)
            #predict_states_in_T_step함수 node.update해서 선형적 모델로 x,y,v,yaw
            #예측함 그래서 만든게 z_bar,, 최적화를 마친 T개의 x,y,v,yaw를 반환함(solve_linear_mpc)

            if delta_opt is not None:
                delta_exc, a_exc = delta_opt[0], a_opt[0] # first index of list

            node.update(a_exc, delta_exc, 1.0)
            
            time += MPC.P.dt

            dist = math.hypot(node.x - cx[-1], node.y - cy[-1])
            # distance of ego to destination
            
            if dist < MPC.P.dist_stop and \
                    abs(node.v) < MPC.P.speed_stop:
                break
            # delta_exc = np.degrees(delta_exc)
            # stop to folow the global path
            # if abs((delta_exc))<0.5:
            #     delta_exc = 0
            # dy = (node.yaw - yaw[-2]) / (node.v * MPC.P.dt)
            # steer = MPC.pi_2_pi(-math.atan(MPC.P.WB * dy))

            self.setValue(10, np.degrees(delta_exc), 0)
            # print("steer: ", self.serial_msg.steer)
            
            self.save_position()
            # if time > 50.0:
            #     plt.show()
            #     plt.plot(self.global_path_x,self.global_path_y,'k-',label='global_path')
            #     plt.plot(self.curPosition_x,self.curPosition_y,'ro',label='present_route',ms=2)
            #     plt.grid()
            #     # plt.legend(loc="lower right")
            #     plt.title("Global_path vs Car_trajectory")
            #     plt.xlabel('x')
            #     plt.ylabel('y')
                
            self.serialWrite()
            # print("serial update: ",self.alive)
            # timetime = time*20
            # if timetime > 255:
            #     timetime = 0
            # print("error: ", self.alive - timetime)
            # print(sp)
            # print(MPC.P.target_speed)
            
            ########################### print values ##############################
            # print("current_x: ", round(node.x,4), "real_x: ", round(self.ego_info.x,4))
            # print("current_y: ", round(node.y,4), "real_y: ", round(self.ego_info.y,4))
            # print("current_yaw: ", round(node.yaw,4), "real_y: ", round(self.ego_info.heading,4))
            print("speed: ", node.v)
            print("delta_exc :", delta_exc)
            # print("steer: ", self.control_input.steer)
            # print("speed: ", self.serial_msg.speed)
            # print("node.v : ", node.v)


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

    def distance(self, x, y):
        return sqrt(x**2+y**2)

    def search_ego_index(self):
        # if self.ego_index is None:
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
        
        self.ego_index = ind
 
        return ind
        

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    erp = Serial_IO().run()
