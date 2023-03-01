#!/usr/bin/env python3
import rospy
import numpy as np
import time
from sensor_msgs.msg import Imu
from ublox_msgs.msg import NavPVT
from planner_and_control.msg import Heading
from lib.local_utils.euler_from_quaternion import euler_from_quaternion as efq
import matplotlib as plt

class Local_test:
    def __init__(self):
        rospy.init_node("/local_test", anonymous = False)
        rospy.Subscriber("/imu", Imu, self.imuCallback)
        rospy.Subscriber("/ublox_gps/navpvt", NavPVT, self.gpsCallback)
        self.pub = rospy.Publisher("/heading", Heading, queue_size = 1)

        self.imu_heading = 0.0
        self.gps_heading = 0.0
        self.heading_gap = 0.0
        self.heading = Heading()

        self.imu_t = 0
        self.gps_t = 0

    def imuCallback(self, data):
        self.imu_t = time.time()
        orientation_q = data.orientation
        roll, pitch, yaw = efq(orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)

        self.imu_heading = np.rad2deg(-1*yaw)

    def gpsCallback(self, data):
        self.gps_t = time.time()
        heading = data.heading
        self.gps_heading = (450 - (heading * 10**(-5))) % 360

    def run(self):
        time_gap = self.imu_t - self.gps_t
        if time_gap <= 0.1:
            self.heading_gap = self.imu_heading - self.gps_heading
            self.heading.imu = self.imu_heading
            self.heading.gps = self.gps_heading
            self.heading.gap = self.heading_gap
            self.pub.publish(self.heading)

if __name__ == "__main__":
    Lt = Local_test()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        Lt.run()
        rate.sleep