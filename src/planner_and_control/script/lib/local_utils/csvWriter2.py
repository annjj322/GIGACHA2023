#!/usr/bin/env python3
import rospy
import csv
import time
# from sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Local
from gps import GPS
from heading import Heading
from ublox_msgs.msg import NavPVT


class Localization():
    def __init__(self):
        rospy.init_node('csvWriter', anonymous=False)
        rospy.Subscriber("/ublox_gps/navpvt", NavPVT, self.gpsCallback)
        # self.gps = GPS()
        self.heading = Heading()

        self.heading_gps = 0
        self.gps_heading = 0

        self.data = []
        self.time_origin = time.time()
        self.time_now = time.time()
        f = open("data2High.csv", "w")
        self.writer = csv.writer(f)

    def gpsCallback(self, data):
        self.heading_gps = data.heading
        self.gps_heading = (450 - (self.heading_gps * 10**(-5))) % 360

    def main(self):
        self.data = [[self.heading.imu_heading, self.gps_heading]]
        self.time_now = time.time()
        delta = self.time_now - self.time_origin
        # print(self.data[0])
        if 4 < delta < 6:
            self.writer.writerow(self.data[0])
            print(delta)

        # if self.heading.headingAcc < 600000:  # gps heading error less than 6 deg
        #     offset = self.heading.gps_heading - self.heading.imu_heading
        #     final_heading = self.heading.imu_heading + offset
        #     rospy.loginfo("Correction Heading : %f" % final_heading)
        # else:
        #     final_heading = self.heading.imu_heading
        #     rospy.loginfo("AHRS Heading : %f" % final_heading)

        # self.msg.x = self.gps.x
        # self.msg.y = self.gps.y
        # self.msg.heading = final_heading

        # rospy.loginfo("=========Localization=========")
        # rospy.loginfo("x : %f" %self.msg.x)
        # rospy.loginfo("y : %f" %self.msg.y)
        # rospy.loginfo("e2box_battery : %f" %self.heading.imu_battery)
        # rospy.loginfo("imuHeading,gpsHeading : %f" % self.data[0])


if __name__ == '__main__':
    # Activate_Signal_Interrupt_Handler()
    loc = Localization()
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()
