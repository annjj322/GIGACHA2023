from turtle import heading
import rospy
import numpy as np
import math
# from euler_from_quaternion import euler_from_quaternion as efq
# from lib.local_utils.low_pass_filter import low_pass_filter as lpf

from sensor_msgs.msg import Imu
from ublox_msgs.msg import NavPVT

class Heading:
    def __init__(self):
        rospy.Subscriber("/imu", Imu, self.imuCallback)
        # rospy.Subscriber("/ublox_gps/navpvt", NavPVT, self.gpsCallback)

        self.imu_heading = 0.0
        self.imu_battery = 0

        self.gps_heading = 0.0
        self.headingAcc = 0.0

    def imuCallback(self, msg):
        orientation_q = msg.orientation
        roll, pitch, yaw = self.euler_from_quaternion(orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)

        imu_heading = np.rad2deg(-1*yaw)
        self.imu_heading = imu_heading % 360
        self.imu_battery = msg.angular_velocity.x

    def gpsCallback(self, msg):
        self.headingAcc = msg.headAcc
        if self.headingAcc < 800000:
            gps_yaw = (450-(msg.heading * 10**(-5)))%360
            # self.gps_heading = lpf(gps_yaw, 30, 0.2)

    def euler_from_quaternion(self, x, y, z, w):
            t0 = +2.0 * (w * x + y * z)
            t1 = +1.0 - 2.0 * (x * x + y * y)
            roll_x = math.atan2(t0, t1)
        
            t2 = +2.0 * (w * y - z * x)
            t2 = +1.0 if t2 > +1.0 else t2
            t2 = -1.0 if t2 < -1.0 else t2
            pitch_y = math.asin(t2)
        
            t3 = +2.0 * (w * z + x * y)
            t4 = +1.0 - 2.0 * (y * y + z * z)
            yaw_z = math.atan2(t3, t4)
        
            return roll_x, pitch_y, yaw_z # in radians

if __name__ == '__main__':
    try:
        Decide_heading=Heading()
    except rospy.ROSInterruptException:
        pass
