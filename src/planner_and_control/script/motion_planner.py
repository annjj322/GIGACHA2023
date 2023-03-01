#!/usr/bin/env python3
import sys,os
from socket import MsgFlag
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.read_global_path import read_global_path
from lib.planner_utils.find_local_path import findLocalPath
from lib.planner_utils.LPP import path_maker

from lib.local_utils.parking_path_maker import findParkingPath
from lib.local_utils.parking_index_finder import ParkingIndexFinder
from planner_and_control.msg import Parking

from planner_and_control.msg import Path as CustomPath
from planner_and_control.msg import Ego
from planner_and_control.msg import Perception
from std_msgs.msg import String
from nav_msgs.msg import Path
from math import sqrt


class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)

        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/perception', Perception, self.perception_callback)
        rospy.Subscriber('/behavior', String, self.behavior_callback)

        self.ego = Ego()
        self.perception = Perception()
        self.global_path = CustomPath()
        self.local_path = Path()
        self.behavior = ''
        
        self.trajectory = CustomPath()
        self.generated_path = Path()
        self.trajectory_name = ""
        self.map_switch = 0

        self.parking = Parking()
        self.forwardPath=CustomPath()
        self.backwardPath=CustomPath()
        self.stack =0
        self.park_pub = rospy.Publisher('/parking', Parking, queue_size = 1)

        self.current_lane = 0
        self.lane_weight = []

        # self.current_lane = int(input("current lane(left : 1, right : 2) : "))

        if self.current_lane == 1:
            self.lane_weight = [10000, 0, 10000]
            self.trajectory.select_lane = int(len(self.lane_weight)/2)
        else:
            self.lane_weight = [10000, 10000, 0]
            self.trajectory.select_lane = 2
        
        # rviz
        self.global_path_pub = rospy.Publisher('/global_path', CustomPath, queue_size = 1)
        self.trajectory_pub = rospy.Publisher('/trajectory', CustomPath, queue_size = 1)
        for i in range(1,4):
            globals()['lattice_path_{}_pub'.format(i)] = rospy.Publisher('lattice_path_{}'.format(i),Path,queue_size=1) 

    def ego_callback(self, msg):
        self.ego = msg
        # if self.map_switch == 0:
        #     print("self.global path is made")
        #     sleep(20000)
        #self.global_path = read_global_path(self.ego.map_folder, self.ego.map_file)

        
            # self.map_switch = 1

    def perception_callback(self, msg):
        self.perception = msg
    
    def behavior_callback(self, msg):
        self.behavior = msg.data

    # avoidance driving
    def weight_function_obstacle_avoidance(self):
        for i in range(len(self.generated_path)): # 0,1,2
            path_check = True
            if path_check == True:
                for j in range(len(self.generated_path[i].poses)): # paths' index
                    if path_check == False:
                        break
                    for k in range(len(self.perception.objx)): # of obj
                        ob_point_distance = sqrt((self.generated_path[i].poses[j].pose.position.x - self.perception.objx[k])**2 + (self.generated_path[i].poses[j].pose.position.y - self.perception.objy[k])**2)
                        if ob_point_distance < self.perception.objr[k]:
                            if(i == 1):
                                self.lane_weight[i] = 10000
                                self.lane_weight[i+1] = 0
                            # elif(i==2):
                            #     self.lane_weight[i] = 10000
                            #     self.lane_weight[i-1] = 0
                            path_check = False
                            break

    # go_to_sign
    def weight_sign_function(self):
        for i in range(len(self.generated_path)):
            self.lane_weight[i] = sqrt((self.generated_path[i].poses[-1].pose.position.x - self.perception.signx[0])**2 + (self.generated_path[i].poses[-1].pose.position.y - self.perception.signy[0])**2)

    def select_trajectory(self):
        # if (len(self.local_path.poses) > 10):
        self.selected_lane = self.lane_weight.index(min(self.lane_weight)) #문제없음
        self.local_path = self.generated_path[self.selected_lane]
        self.trajectory_name = self.selected_lane

        tmp_trajectory = CustomPath()
        for i in range (len(self.local_path.poses)):
            tmp_trajectory.x.append(self.local_path.poses[i].pose.position.x)
            tmp_trajectory.y.append(self.local_path.poses[i].pose.position.y)
        self.trajectory = tmp_trajectory
        
        print(f"lane_weight : {self.lane_weight}")
        if self.selected_lane == 1:
            print(f"motion_planner : global_path")
        else:
            print(f"motion_planner : selected lane {self.trajectory_name}, local_path")

    def make_parking_trajectory(self):
        if self.stack==0 and self.map_switch==1:
            # self.forwardPath, self.backwardPath = findParkingPath(self.global_path,self.ego)
            self.forwardPath, self.backwardPath = findParkingPath(self.global_path,self.ego)
            self.parking.on = True
            self.stack = 1
        self.trajectory = self.forwardPath
        # self.trajectory = self.backwardPath
        self.PIF = ParkingIndexFinder(self.ego,self.trajectory)
        self.parking.index = self.PIF.run()
        self.park_pub.publish(self.parking)
        print(self.parking.index)

    def run(self):
        
        self.global_path = read_global_path(self.ego.map_folder, self.ego.map_file)
        self.local_path = findLocalPath(self.global_path, self.ego) # local path (50)
        
        ## jm added
        while 1:
            if len(self.local_path.poses) == 1:
                self.local_path = findLocalPath(self.global_path, self.ego)
            else:
                break
        ##

        self.generated_path = path_maker(self.local_path, self.ego) # lattice paths
       

        if self.behavior == "static_obstacle_avoidance":
            self.weight_function_obstacle_avoidance()
            self.select_trajectory()
        
        elif self.behavior == "go_side":
            self.weight_sign_function()
            self.select_trajectory()
        
        elif self.behavior == "stop":
            self.trajectory.x = []
            self.trajectory.y = []

        elif self.behavior == "turn_right":
            self.lane_weight = [10000, 10000, 0]
            self.select_trajectory()

        elif self.behavior == "turn_left":
            self.lane_weight = [10000, 0, 10000]
            self.select_trajectory()

        else:  ## self.behavior == "go"
            self.select_trajectory()
            # self.make_parking_trajectory()

        
        # path publish
        self.trajectory.select_lane = self.selected_lane
        self.global_path_pub.publish(self.global_path)
        self.trajectory_pub.publish(self.trajectory)
        #print(f"trajectory : {self.trajectory.x}")
        if len(self.generated_path) == 3:
            for i in range(1,4):
                globals()['lattice_path_{}_pub'.format(i)].publish(self.generated_path[i-1])


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mp = Motion_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mp.run()
        rate.sleep()
