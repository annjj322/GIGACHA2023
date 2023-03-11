#!/usr/bin/env python3
from sig_int_handler import Activate_Signal_Interrupt_Handler
import serial
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from local_pkg.msg import Local
import threading
import struct
import rospy
from math import sqrt, atan2, sin
from numpy import degrees, radians, argmin, hypot
import numpy as np
import json
from geometry_msgs.msg import PoseArray

class Serial_IO:
    def __init__(self):
        self.count = 0
        self.count2 = 0
        self.k = 0.55
        self.WB = 1.04 # wheel base
        self.lookahead_default = 1
        self.global_path_x = []
        self.global_path_y = []
        ################### JMGAY : No TOUCH!! ####################
        ###########################################################
        # Serial Connect
        self.ser = serial.Serial("/dev/erp42", 115200) # Real World

        # ROS Publish
        rospy.init_node("Serial_IO", anonymous=False)
        self.serial_pub = rospy.Publisher("/serial", Serial_Info, queue_size=1)
       
        # Messages/Data
        self.serial_msg = Serial_Info()  # Message o publish
        self.alive = 0

####################### jyjy made. Don't touch my body !!!! ############################
        # Subscribing Ego information
        rospy.Subscriber("/local_msgs", Local, self.localcallback)
        
        # Subscribing Obstacle position information
        rospy.Subscriber('jm',PoseArray,self.obstaclecallback)
        
        # Reading Global Path
        self.read_global_path()
        self.ego_info = Local()
        # Reading Obstacle Position
        self.obstacle_info = PoseArray()
        # Pure Pursuit coefficient
        self.old_nearest_point_index = None
########################################################################################

        # Serial Read Thread
        th_serialRead = threading.Thread(target=self.serialRead)
        th_serialRead.daemon = True
        th_serialRead.start()

        # rospy Rate
        self.rt = 20
        
        self.control_input = Control_Info()
        self.dx = []
        self.dy = []
        #############################################################
        #############################################################


        ### touch me... haang...
        self.control_input.speed = 5 # chogi speed
        # self.control_input.steer = 2 # chogi steer : going a little left when steer is 0, so 1(change it!)
        self.control_input.brake = 0 # chogi brake
     
        # Main Loop
        sprint_time_sec = 5 # touch me!
        brake_freq_sec = 0.75 # touch me!


    def run(self):
        rate = rospy.Rate(self.rt)
        while not rospy.is_shutdown():
            print("hi ", self.old_nearest_point_index)
            print()
            self.control_input.steer = self.Pure_pursuit()
            self.serialWrite()
            rate.sleep()
        #     self.count += 1
        #     self.count2 += 1
        #     if self.count2>=(sprint_time_sec*rt) and self.count%(brake_freq_sec*rt)==0: # 5sec full sprint, brake+=10 per 0.75sec
        #         self.control_input.brake+=10
        #     self.serialWrite()
        #     rate.sleep()


    def serialRead(self):
        print("Serial_IO: Serial reading thread successfully started")

        while True:
            
            print(f"Serial_IO: Reading serial {self.alive}")

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
            self.control_input.brake,
            self.alive,
            0x0D,
            0x0A
        )
        self.ser.write(result)
################################## hyjy Don't touch me !!!jm is touching yummy############################################################    
    def localcallback(self,msg):
        self.ego_info.x = msg.x
        self.ego_info.y = msg.y
        self.ego_info.heading = msg.heading
        self.ego_info.speeed = msg.speeed

    def obstaclecallback(self,msg):
        self.obstacle_info.x = msg.x
        self.obstacle_info.y = msg.y
        
    def read_global_path(self):
        with open(f"/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/Inha_Songdo/songdo_jikjin_course.json", 'r') as json_file:
            json_data = json.load(json_file)
            for n, (x, y, mission, map_speed) in enumerate(json_data.values()):
                self.global_path_x.append(x)
                self.global_path_y.append(y)

    def calc_distance(self, point_x, point_y):
        dx = self.ego_info.x - point_x
        dy = self.ego_info.y - point_y
        d= np.hypot(dx,dy)
        return d

    def distance(self, x, y):
        return sqrt(x**2+y**2)

    def search_target_index(self):
        # if self.old_nearest_point_index is None:
        d = []
        for i in range(len(self.global_path_x)):
            self.dx.append(self.ego_info.x - self.global_path_x[i])
            self.dy.append(self.ego_info.y - self.global_path_y[i])
        
        for i in range(len(self.dx)):
            d.append(self.distance(self.dx[i], self.dy[i]))
        
        new_d = np.array(d)
        ind = np.argmin(new_d)
        self.dx = []
        self.dy = []
        #     self.old_nearest_point_index = ind
        # else:
        #     ind = self.old_nearest_point_index
        #     distance_this_index = self.calc_distance(self.dx[ind], self.dy[ind])
        #     while True:
        #         distance_next_index = self.calc_distance(self.global_path_x[ind + 1], self.global_path_y[ind + 1])
        #         if distance_this_index < distance_next_index:
        #             break
        #         print("going to next point")
        #         ind = ind + 1 if (ind + 1) < len(self.global_path_x) else ind
        #         distance_this_index = distance_next_index
        
        #     self.old_nearest_point_index = ind

        Lf = self.k * self.ego_info.speeed + self.lookahead_default  # update look ahead distance

        # search look ahead target point index
        while Lf > self.calc_distance(self.global_path_x[ind], self.global_path_y[ind]):
            if (ind + 1) >= len(self.global_path_x):
                break  # not exceed goal
            ind += 1

        return ind, Lf

    def Pure_pursuit(self):
        ind,Lf=self.search_target_index()
        lookahead = min(Lf, 6)
        target_index = ind  #self.ego_info.x'''''' + 49
        
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

    # def controlCallback(self, msg):
    #     self.control_input = msg

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    erp = Serial_IO().run()
