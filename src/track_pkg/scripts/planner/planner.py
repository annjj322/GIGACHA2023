#!/usr/bin/env python3
import threading
from math import hypot
from time import sleep
from std_msgs.msg import String
from math import pi, cos, sin
from visualization_msgs.msg import MarkerArray, Marker
import rospy

class Planner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.global_path = self.shared.global_path

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.state = self.shared.state
        self.total_obs = []


    def makePath(self):        
        self.perception.left_obs.sort(key = lambda x : x[2])
        self.perception.right_obs.sort(key= lambda x : x[2])


        # 왼쪽에서 인식한 러버콘수가 2개초과이면 2개만 남긴다 그 뒤 오른쪽에서 인식한 러버콘 수가 2개 초과이면 2개만 남긴다.
        if len(self.perception.left_obs) > 2:
            self.perception.left_obs = self.perception.left_obs[0:2]   

        if len(self.perception.right_obs) > 2:
            self.perception.right_obs=self.perception.right_obs[0:2]
        
        # concat all obstacle
        self.total_obs = self.perception.left_obs + self.perception.right_obs

        # (2,2), (2,1), (1,2), (1,1) case
        if len(self.perception.left_obs) != 0 and len(self.perception.right_obs) != 0:
            if len(self.perception.left_obs) != len(self.perception.right_obs):
                self.makeCOM(self.perception.left_obs, self.perception.right_obs)
            else:              
                self.makeCOM(self.perception.left_obs, self.perception.right_obs)
        # (2,0), (1,0), (0,1), (0,2)
        elif len(self.perception.left_obs) == 0 or len(self.perception.right_obs) == 0:
            self.makeFakeCOM(self.perception.left_obs, self.perception.right_obs)
        else:   # (0, 0) case
            pass



    def makeCOM(self, left_points, right_points):
        lpointx=0
        lpointy=0
        rpointx=0
        rpointy=0

        for point in left_points:
            lpointx+=point[0]
            lpointy+=point[1]

        for point in right_points:
            rpointx+=point[0]
            rpointy+=point[1]

        try:
            self.ego.point_x=(lpointx+rpointx)/(len(left_points)+len(right_points))
            self.ego.point_y=(lpointy+rpointy)/(len(left_points)+len(right_points))
        except ZeroDivisionError:
            #print("ZeroDivisionError")
            pass
    
    # (2,0), (1,0), (0,2), (0,1) case
    def makeFakeCOM(self, left_points, right_points):
        fake_point_list = []
        # right case
        if len(left_points) == 0:
            for rpoint in right_points:
                fake_point_list.append([rpoint[0]-0.4, rpoint[1]+3.5, rpoint[2], rpoint[3]])
            self.makeCOM(fake_point_list, right_points)
        # left case
        elif len(right_points) == 0:
            for lpoint in left_points:
                fake_point_list.append([lpoint[0]-0.4, lpoint[1]-3.5, lpoint[2], lpoint[3]])
            self.makeCOM(left_points, fake_point_list)
        else:
            rospy.loginfo("Failed to classificate in FakeCOM")

    def run(self):
        while True:
            # try:
            self.makePath()
        
            # except IndexError:
                # print("+++++++++Planner++++++++")
            
            sleep(self.period)
