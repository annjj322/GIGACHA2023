#!/usr/bin/env python3
import threading
import rospy
import pandas as pd
from time import sleep
from math import hypot
from std_msgs.msg import Int64
from sensor_msgs.msg import Imu
from local_pkg.msg import Serial_Info

class MC(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.map_switch = False
        self.period = 1.0 / rate
        self.global_path = parent.shared.global_path
        self.shared = parent.shared

        self.ego = parent.shared.ego

        self.right = 0  # pulse from sensor
        self.left = 0  # pulse from serial

        # for odometry
        self.init = 0
        self.flag_filter = True

        self.left_pulse = 0
        self.right_pulse = 0
        self.pulse = 0
        self.diff_left = 0
        self.diff_right = 0

        self.stop_thread = False
        self.right_switch = False
        self.temp = 0

        self.x = []
        self.y = []

        self.prev_x = 0
        self.prev_y = 0

        rospy.Subscriber('/Displacement_right', Int64, self.encoderCallback)
        rospy.Subscriber('/imu', Imu, self.map_csv)
        rospy.Subscriber('/serial', Serial_Info, self.serialTopulse)

    def serialTopulse(self, data):  
        if self.init == 0: 
            self.init = int(data.encoder[0]) + int(data.encoder[1])*256 \
                 + int(data.encoder[2])*256**2 + \
                    int(data.encoder[3])*256**3 
 
        self.left = int(data.encoder[0]) + int(data.encoder[1])*256 \
             + int(data.encoder[2])*256**2 + \
                int(data.encoder[3])*256**3 - self.init 

        self.filter()

    def filter(self):
        if self.flag_filter:
            self.left_pulse = self.left
            self.right_pulse = self.right
            self.flag_filter = False

        if (abs(self.left - self.left_pulse) > 100):
            self.left_pulse = self.left + self.diff_left
        else:
            self.diff_left = self.left - self.left_pulse
            self.left_pulse = self.left

        if (abs(self.right - self.right_pulse) > 100):
            self.right_pulse = self.right + self.diff_right
        else:
            self.diff_right = self.right - self.right_pulse
            self.right_pulse = self.right

    def encoderCallback(self,msg):
        if self.right_switch == False:
            self.right_init = msg.data
            self.right_switch = True

        self.right = msg.data - self.right_init

        # print(self.right)

        self.pulse = (self.right_pulse + self.left_pulse) / 2

    def map_maker(self):
        self.temp = self.pulse

        if self.ego.x != self.prev_x and self.ego.y != self.prev_y:
            self.x.append(self.ego.x)
            self.y.append(self.ego.y)

        self.prev_x = self.ego.x
        self.prev_y = self.ego.y

    def map_csv(self, msg):
        print('subscripve--------------------------------')
        if self.map_switch == False:
            save_data = list(zip(self.x, self.y))

            save_df = pd.DataFrame(save_data)
            save_df.to_csv("parking_parallel.csv", index = False, header = False)
            self.map_switch = True    

    def run(self):
        while True:
            if not self.stop_thread:
                if round(self.pulse) % 6 == 0 and self.pulse != self.temp:
                    self.map_maker()
            else:
                sleep(self.period)