#!/usr/bin/env python3
import threading
import rospy
import pandas as pd
import pymap3d
import json
from time import sleep
from math import hypot
from sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import Int64
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from local_pkg.msg import Serial_Info


class MC():
    def __init__(self):
        rospy.init_node('Map_maker', anonymous = False)
        self.map_switch = False
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
        rospy.Subscriber("ublox_gps/fix", NavSatFix, self.gps_call_back)

        with open('/home/gigacha/TEAM-GIGACHA/src/local_pkg/scripts/base.json') as base:
            base_data = json.load(base)

        self.base = base_data['Siheung']  # KCity, Siheung, KCity_semi,
        self.lat = self.base['lat']
        self.lon = self.base['lon']
        self.alt = self.base['alt']

    def gps_call_back(self, data):
        # self.gps_x, self.gps_y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, self.alt,
        #                                                  self.lat, self.lon, self.alt)
        self.gps_x = data.longitude
        self.gps_y = data.latitude

    def serialTopulse(self, data):

        left_pulse = int(data.encoder[0]) + int(data.encoder[1])*256 \
            + int(data.encoder[2])*256**2 + \
            int(data.encoder[3])*256**3

        if 0 <= left_pulse <= 255:
            left_pulse = 256**4 - 1 + left_pulse

        if self.init == 0:
            self.init = left_pulse

        self.left = left_pulse - self.init

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

    def encoderCallback(self, msg):
        if self.right_switch == False:
            self.right_init = msg.data
            self.right_switch = True

        self.right = msg.data - self.right_init

        # print(self.right)

        self.pulse = (self.right_pulse + self.left_pulse) / 2

    def map_maker(self):
        self.temp = self.pulse

        if self.gps_x != self.prev_x and self.gps_y != self.prev_y:
            self.x.append(self.gps_x)
            self.y.append(self.gps_y)

        self.prev_x = self.gps_x
        self.prev_y = self.gps_y

    def map_csv(self, msg):
        print('subscripve--------------------------------')
        if self.map_switch == False:
            save_data = list(zip(self.x, self.y))

            save_df = pd.DataFrame(save_data)
            save_df.to_csv("new_semi2.csv", index=False, header=False)
            self.map_switch = True

    def main(self):
        if self.map_switch != True:
            if round(self.pulse) % 6 == 0 and self.pulse != self.temp:
                self.map_maker()


if __name__ == '__main__':
    Activate_Signal_Interrupt_Handler()

    loc = MC()
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()
