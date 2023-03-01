#!/usr/bin/env python3
import math
import rospy
import time
import numpy as np
from local_pkg.msg import Displacement

class DR_enc():
    def __init__(self, ego):
        rospy.Subscriber('/encoder', Displacement, self.encoderCallback)
        self.ego = ego
        
        self.t_old = time.time()
        self.t_new = time.time()
        self.t_delta = self.t_new - self.t_old  
        self.new_loc = []
        self.routes = [] 

        self.theta = 0
        self.transitional_velocity = 0
        self.rotational_velocity = 0

        self.rotate_right = 0
        self.rotate_left = 0 
        self.radius_wheel = 0.25
        self.distance_btw_wheel = 0.97

    def serialTopulse(self):
        if self.init == 0:
            self.init = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
                + int(self.ego.encoder[2])*256**2 + \
                int(self.ego.encoder[3])*256**3

        odometry_left = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
            + int(self.ego.encoder[2])*256**2 + \
            int(self.ego.encoder[3])*256**3 - self.init

        return odometry_left/100
        
    ### 현재 위치 계산 함수
    def calc_location(self):
        self.rotate_right = self.rotate_right_callback
        self.rotate_left = self.rotate_left_callback

        self.t_old = self.t_new
        self.t_new = time.time()
        self.t_delta = float(self.t_new - self.t_old)

        self.transitional_velocity = self.radius_wheel * (self.rotate_right + self.rotate_left) / (2 * self.t_delta)
        self.rotational_velocity = self.radius_wheel * (self.rotate_right - self.rotate_left) / (2 * self.distance_btw_wheel)

        self.theta = self.routes[-1][3] + self.rotational_velocity*self.t_delta

        if self.rotational_velocity==0:
            #runge-kutta integration
            self.ego.dr_x = self.routes[-1][1] + self.transitional_velocity*self.t_delta*math.cos(self.theta + (self.rotational_velocity*self.t_delta)/2)
            self.ego.dr_y = self.routes[-1][2] + self.transitional_velocity*self.t_delta*math.sin(self.theta + (self.rotational_velocity*self.t_delta)/2)
        else:
            self.ego.dr_x = self.routes[-1][1] + (self.transitional_velocity/self.rotational_velocity) * (math.sin(self.routes[-1][3]) - math.sin(self.theta))
            self.ego.dr_y = self.routes[-1][2] - (self.transitional_velocity/self.rotational_velocity) * (math.cos(self.routes[-1][3]) - math.cos(self.theta))

        self.new_loc = [self.t_now, self.ego.dr_x, self.ego.dr_y, self.theta, self.transitional_velocity, self.rotational_velocity, self.t_delta]
        
        self.routes.append(self.new_loc)

    def encoderCallback(self, msg):
        self.rotate_right_callback = msg.data/100
        self.rotate_left_callback = self.serialTopulse()

        self.calc_location()

if __name__ == '__main__':
    try:
        dr_enc = DR_enc()
    except rospy.ROSInitException:
        pass