#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from math import sqrt
import rospy
from geometry_msgs.msg import Point, PoseArray
from visualization_msgs.msg import MarkerArray, Marker
from sensor_msgs.msg import PointCloud 
import itertools as it
import numpy as np

class Perception_():
   def __init__(self):
      rospy.Subscriber("/cone_blue", PoseArray, self.blue_callback)
      rospy.Subscriber("/cone_yellow", PoseArray, self.yellow_callback)
      self.left_obs = []
      self.right_obs = []
      self.roi_dist = 6.0

   def calc_distance(self, obs_x, obs_y):
        p1 = [0, 0]
        p2 = [obs_x, obs_y]
        dis = sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p1, p2)))
        return dis

   def yellow_callback(self, msg):
        obstacles=[]
        
        for point in msg.poses:
            tmp_obs_dis = self.calc_distance(point.orientation.x, point.orientation.y)
            if tmp_obs_dis < self.roi_dist:
               obstacles.append([round(point.orientation.x, 2), round(point.orientation.y, 2), round(tmp_obs_dis, 2), point.orientation.w]) # x좌표,y좌표,거리좌표,객체id(0==y, 1==b)
        
        self.left_obs= obstacles

   def blue_callback(self, msg):
        obstacles=[]
        
        for point in msg.poses:
            tmp_obs_dis = self.calc_distance(point.orientation.x, point.orientation.y)
            if tmp_obs_dis < self.roi_dist:
               obstacles.append([round(point.orientation.x, 2), round(point.orientation.y, 2), round(tmp_obs_dis, 2), point.orientation.w]) # x좌표,y좌표,거리좌표,객체id(0==y, 1==b)
        
        self.right_obs= obstacles