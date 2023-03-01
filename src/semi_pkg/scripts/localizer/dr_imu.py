#!/usr/bin/env python3
import math
import rospy
import time
import numpy as np
from local_pkg.msg import Displacement

class DR_imu():
    def __init__(self, ego, imu):
        rospy.Subscriber('/encoder', Displacement, self.encoderCallback)
        self.imu = imu
        self.ego = ego
        
        self.t_old = time.time()
        self.t_new = time.time()
        self.t_delta = self.t_new - self.t_old 
        self.new_loc = []
        self.routes = []

        self.theta = 0
        self.transitional_velocity = 0.0

        self.linear_accel_x = 0.0
        self.linear_accel_y = 0.0

    def calc_location(self):
        self.linear_accel_x = self.imu.linear_accel_x
        self.linear_accel_y = self.imu.linear_accel_y
        self.delta_theta = self.imu.angular_velocity_z

        ### 시간 업데이트
        self.t_old = self.t_new
        self.t_new = time.time()
        self.t_delta = float(self.t_new - self.t_old)

        self.transitional_velocity = math.sqrt((self.linear_accel_x*self.t_delta)**2 + (self.linear_accel_y*self.t_delta)**2)
        print("v=", self.transitional_velocity)

        self.ego.dr_x = self.routes[-1][1] + self.transitional_velocity * math.sin(np.deg2rad(self.ego.heading)) * self.t_delta
        self.ego.dr_y = self.routes[-1][2] + self.transitional_velocity * math.cos(np.deg2rad(self.ego.heading)) * self.t_delta

        self.new_loc = [self.t_now, self.ego.dr_x, self.ego.dr_y, self.theta, self.transitional_velocity, np.deg2rad(self.ego.heading), self.t_delta]

        self.routes.append(self.new_loc)

    def encoderCallback(self):
        self.calc_location()

if __name__ == '__main__':
    try:
        dr_imu = DR_imu()
    except rospy.ROSInitException:
        pass