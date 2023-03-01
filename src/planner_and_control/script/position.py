#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose, PoseStamped
from planner_and_control.msg import Local
from sensor_msgs.msg import NavSatFix, Imu
from ublox_msgs.msg import NavPVT

import pymap3d

import numpy as np
import math

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)
        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        self.msg = Local()

        #Visualization
        self.vis_pub = rospy.Publisher('/vis_pose', PoseStamped, queue_size=1)
        self.vis_msg = PoseStamped()
        self.vis_msg.header.frame_id = "map"
        
        #KCity
        # self.lat_origin = 37.239231667
        # self.lon_origin = 126.773156667
        # self.alt_origin = 15.400
        
        # #Songdo
        self.lat_origin = 37.3843177 
        self.lon_origin = 126.6553022
        self.alt_origin = 15.4

        # simul
        # self.lat_origin = 37.239235 
        # self.lon_origin = 126.77315833333333
        # self.alt_origin = 15.4        

        self.yaw_gps = 0
        self.yaw_imu = 0
        self.yaw_rate = 0

        rospy.Subscriber("/simul_gps", Pose, self.gps_call_back)
        rospy.Subscriber("/simul_imu", Pose, self.imu_call_back)
        
        rospy.Subscriber('/ublox/navpvt',NavPVT, self.gps_Heading)
        rospy.Subscriber("/ublox/fix", NavSatFix, self.gps_call_back)
        rospy.Subscriber("/imu", Imu, self.imu_call_back)

    def gps_call_back(self, data):
        self.msg.x, self.msg.y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, self.alt_origin, \
                                            self.lat_origin , self.lon_origin, self.alt_origin)

    def imu_call_back(self, data):
        self.vis_msg.pose.orientation = data.orientation
        self.yaw_rate = -data.angular_velocity.z

        orientation_q = data.orientation
        roll, pitch, yaw = self.euler_from_quaternion(orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)

        self.yaw_imu = np.rad2deg(-1 * yaw)
        
    def gps_Heading(self, data):
        self.yaw_gps = data.heading

    def euler_from_quaternion(self,x, y, z, w):
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

    def main(self):
        self.msg.heading = self.yaw_imu
        self.pub.publish(self.msg)

        self.vis_msg.pose.position.x = self.msg.x
        self.vis_msg.pose.position.y = self.msg.y
        self.vis_msg.header.stamp = rospy.Time.now()
        self.vis_pub.publish(self.vis_msg)

        print("self.yaw_imu:{}".format(self.yaw_imu))

if __name__ == '__main__':
    loc = Localization()
    rate = rospy.Rate(100)
 
    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()