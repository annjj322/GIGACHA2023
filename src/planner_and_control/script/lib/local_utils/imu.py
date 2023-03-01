#!/usr/bin/env python3
import rospy
import numpy as np

from lib.local_utils.euler_from_quaternion import euler_from_quaternion as efq
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Pose

class IMU():
    def __init__(self):
        self.yaw = 0
        self.yaw_rate = 0
        self.battery = 0
        
        rospy.Subscriber("/imu", Imu, self.imu_call_back)

    def imu_call_back(self, data):

        orientation_q = data.orientation
        roll, pitch, yaw = efq(orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)

        self.yaw = np.rad2deg(-1*yaw)
        self.battery = data.angular_velocity.x

if __name__ == '__main__':
    try:
        imu=IMU()
    except rospy.ROSInterruptException:
        pass