#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
from nav_msgs.msg import Path,Odometry
from geometry_msgs.msg import PoseStamped,Point
from std_msgs.msg import Float64,Int16,Float32MultiArray
import numpy as np
from math import cos,sin,sqrt,pow,atan2,pi
import tf
from ...mission_planner import Mission_Planner

class LPP:
    def __init__(self):
        self.out_path = []
        self.selected_lane = 0
        self.look_distance = 0
        self.global_ref_start_point = ()
        self.global_ref_start_next_point = ()
        self.global_ref_end_point = ()
        self.theta = 0
        self.translation = []
        self.t = np.array([[]])
        self.det_t = np.array([[]])
        self.world_end_point = np.array([[]])
        self.local_end_point = np.array([[]])
        self.world_ego_vehicle_position = np.array([[]])
        self.local_ego_vehicle_position = np.array([[]])
        self.lane_off_set=[]
        self.local_lattice_points=[]
        self.end_point = 0
        self.lattice_path = Path()
        self.lattice_path.header.frame_id=''
        self.x = []
        self.y = []
        self.x_interval = 0
        self.xs = 0
        self.ps = 0
        self.pf = 0
        self.x_num = 0
        self.lane_num = 0 
        self.result = 0 
        self.local_result = np.array([[]])
        self.global_result = np.array([[]])
        self.read_pose = PoseStamped()
        self.lane_weight= [2,0]
        


    def obstacle_distance(self):
        self.MP = Mission_Planner()
        self.global_vaild_object = self.MP.obs_dis

    def latticePlanner(self, ref_path, global_vaild_object, vehicle_status, speed, current_lane):
        self.selected_lane = -1
        self.look_distance = int(speed*0.5)

        if self.look_distance < 5 :
            self.look_distance = 5    
        if self.look_distance > 8 :
            self.look_distance = 8   

        if len(ref_path.poses) > self.look_distance :
            self.global_ref_start_point=(ref_path.poses[0].pose.position.self.x,ref_path.poses[0].pose.position.self.y)
            self.global_ref_start_next_point=(ref_path.poses[1].pose.position.self.x,ref_path.poses[1].pose.position.self.y)
            self.global_ref_end_point=(ref_path.poses[self.look_distance].pose.position.self.x,ref_path.poses[self.look_distance].pose.position.self.y)
            
            self.theta = atan2(self.global_ref_start_next_point[1]-self.global_ref_start_point[1],self.global_ref_start_next_point[0]-self.global_ref_start_point[0])
            self.translation=[self.global_ref_start_point[0],self.global_ref_start_point[1]]

            self.t=np.array([[cos(self.theta), -sin(self.theta),self.translation[0]],[sin(self.theta),cos(self.theta),self.translation[1]],[0,0,1]])
            self.det_t=np.array([[self.t[0][0],self.t[1][0],-(self.t[0][0]*self.translation[0]+self.t[1][0]*self.translation[1])   ],[self.t[0][1],self.t[1][1],-(self.t[0][1]*self.translation[0]+self.t[1][1]*self.translation[1])   ],[0,0,1]])



            self.world_end_point=np.array([[self.global_ref_end_point[0]],[self.global_ref_end_point[1]],[1]])
            self.local_end_point=self.det_t.dot(self.world_end_point)
            self.world_ego_vehicle_position=np.array([[vehicle_status[0]],[vehicle_status[1]],[1]])
            self.local_ego_vehicle_position=self.det_t.dot(self.world_ego_vehicle_position)
            self.lane_off_set=[1.0,0]
            for i in range(len(self.lane_off_set)):
                self.local_lattice_points.append([self.local_end_point[0][0],self.local_end_point[1][0]+self.lane_off_set[i],1])
                


            for self.end_point in self.local_lattice_points :
                self.lattice_path.header.frame_id='map'
                self.xf = self.end_point[0]
                self.ps = self.local_ego_vehicle_position[1][0]
                self.pf = self.end_point[1]
                self.x_num = self.xf/self.x_interval

                for i in range(self.xs,int(self.x_num)) : 
                    self.x.append(i*self.x_interval)
                
                a=[0.0,0.0,0.0,0.0]
                a[0]=self.ps
                a[1]=0
                a[2]=3.0*(self.pf-self.ps)/(self.xf*self.xf)
                a[3]=-2.0*(self.pf-self.ps)/(self.xf*self.xf*self.xf)

                for i in self.x:
                    self.result=a[3]*i*i*i+a[2]*i*i+a[1]*i+a[0]
                    self.y.append(self.result)


                for i in range(0,len(self.y)) :
                    self.local_result=np.array([[self.x[i]],[self.y[i]],[1]])
                    self.global_result=self.t.dot(self.local_result)

                    self.read_pose=PoseStamped()
                    self.read_pose.pose.position.self.x=self.global_result[0][0]
                    self.read_pose.pose.position.self.y=self.global_result[1][0]
                    self.read_pose.pose.position.z=0
                    self.read_pose.pose.orientation.self.x=0
                    self.read_pose.pose.orientation.self.y=0
                    self.read_pose.pose.orientation.z=0
                    self.read_pose.pose.orientation.w=1
                    self.lattice_path.poses.append(self.read_pose)

                self.out_path.append(self.lattice_path) # 여기까지 수정했습니다 준영님
            
            add_point_size=int(vehicle_status[3]*4*3.6)
            if add_point_size>len(ref_path.poses)-2:
                add_point_size=len(ref_path.poses)
            elif add_point_size<10 :
                add_point_size=10
            
            
            
            for i in range(self.look_distance,add_point_size):
                if i+1 < len(ref_path.poses):
                    tmp_theta=atan2(ref_path.poses[i+1].pose.position.self.y-ref_path.poses[i].pose.position.self.y,ref_path.poses[i+1].pose.position.self.x-ref_path.poses[i].pose.position.self.x)
                    
                    tmp_translation=[ref_path.poses[i].pose.position.self.x,ref_path.poses[i].pose.position.self.y]
                    tmp_t=np.array([[cos(tmp_theta), -sin(tmp_theta),tmp_translation[0]],[sin(tmp_theta),cos(tmp_theta),tmp_translation[1]],[0,0,1]])
                    tmp_det_t=np.array([[tmp_t[0][0],tmp_t[1][0],-(tmp_t[0][0]*tmp_translation[0]+tmp_t[1][0]*tmp_translation[1])   ],[tmp_t[0][1],tmp_t[1][1],-(tmp_t[0][1]*tmp_translation[0]+tmp_t[1][1]*tmp_translation[1])   ],[0,0,1]])

                    for self.lane_num in range(len(self.lane_off_set)) :
                        self.local_result=np.array([[0],[self.lane_off_set[self.lane_num]],[1]])
                        self.global_result=tmp_t.dot(self.local_result)

                        self.read_pose.pose.position.self.x=self.global_result[0][0]
                        self.read_pose.pose.position.self.y=self.global_result[1][0]
                        self.read_pose.pose.position.z=0
                        self.read_pose.pose.orientation.self.x=0
                        self.read_pose.pose.orientation.self.y=0
                        self.read_pose.pose.orientation.z=0
                        self.read_pose.pose.orientation.w=1
                        self.out_path[self.lane_num].poses.append(self.read_pose)

            self.lane_weight=[2,0] #reference path 
            collision_bool=[False,False]

            if len(global_vaild_object)>0:

                for obj in global_vaild_object :
                    if  obj[0]==2 or obj[0]==1 : 
                        for path_num in range(len(self.out_path)) :
                            
                            for path_pos in self.out_path[path_num].poses :
                                
                                dis= sqrt(pow(obj[1]-path_pos.pose.position.self.x,2)+pow(obj[2]-path_pos.pose.position.self.y,2))
    
                                if dis<1.0:
                                    collision_bool[path_num]=True
                                    self.lane_weight[path_num]=self.lane_weight[path_num]+100
                                    break
            else :
                print("No Obstacle")
        
            selected_lane=self.lane_weight.index(min(self.lane_weight))
            print(self.lane_weight,selected_lane)
            all_lane_collision=True
            
        else :
            print("NO Reference Path")
            selected_lane=-1    
            




        return self.out_path,selected_lane
