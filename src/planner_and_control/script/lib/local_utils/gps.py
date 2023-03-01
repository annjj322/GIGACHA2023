#!/usr/bin/env python3
import rospy
import pymap3d
# from planner_and_control.msg import Gngga
from sensor_msgs.msg import NavSatFix

class GPS():
    def __init__(self):
        # rospy.Subscriber("/Gngga_raw", Gngga, self.gps_call_back)
        rospy.Subscriber("/ublox_gps/fix", NavSatFix, self.gps_call_back)
        
        self.x = 0
        self.y = 0
        self.yaw_gps = 0

        self.base = rospy.get_param("Kcity") # KCity, Songdo, Songdo_track, Siheung
        self.lat = self.base['lat']
        self.lon = self.base['lon']
        self.alt = self.base['alt']

    def gps_call_back(self, data):
        self.x, self.y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, self.alt, \
                                            self.lat, self.lon, self.alt)

        # self.cov_x_gps = data.position_covariance[4]
        # self.cov_y_gps = data.position_covariance[0]
        # self.cov_xy_gps = data.position_covariance[1] ### for kalman filter

if __name__ == '__main__':
    try:
        gps=GPS()
    except rospy.ROSInterruptException:
        pass