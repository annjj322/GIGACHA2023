#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan,PointCloud
from math import cos,sin,pi
from geometry_msgs.msg import Point32
from planner_and_control.msg import Ego

class lidarParser :

    def __init__(self):
        rospy.init_node('lidar_parser', anonymous=True)
        rospy.Subscriber("/scan", LaserScan, self.laser_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)

        self.pcd_pub = rospy.Publisher('/2d_lidar',PointCloud, queue_size=1)
        self.pcd_coordi_pub = rospy.Publisher('/pcl',PointCloud, queue_size=1)
        
        self.ego = Ego()

        rospy.spin()
        
    def ego_callback(self, msg):
        self.ego = msg

    def laser_callback(self,msg):
        pcd = PointCloud()
        pcd_roi = PointCloud()
        pcd_coordi = PointCloud()

        pcd.header.frame_id = "world"
        pcd_roi.header.frame_id = msg.header.frame_id
        pcd_coordi.header.frame_id = msg.header.frame_id
        
        angle=0
        
        # 축 변환
        for r in msg.ranges :
            tmp_point=Point32()
            t_point=Point32()
            tmp_point.x=r*cos(angle)
            tmp_point.y=r*sin(angle)
            t_point.x = tmp_point.x * cos(3*pi/2) - tmp_point.y * sin(3*pi/2)
            t_point.y = tmp_point.x * sin(3*pi/2) + tmp_point.y * cos(3*pi/2)
            angle = angle+(0.0032287694048136473)
            pcd.points.append(t_point)
            
        # roi 설정
        for i in range(len(pcd.points)):
            tmp_point_2 = Point32()
            # if (pcd.points[i].x < 0.75 and pcd.points[i].x > -0.75) and (pcd.points[i].y < 10 and pcd.points[i].y > 0):
            if (pcd.points[i].y > 0):
                tmp_point_2.x = pcd.points[i].x
                tmp_point_2.y = pcd.points[i].y
                pcd_roi.points.append(tmp_point_2)
        
        theta = (self.ego.heading) * pi / 180
                
        for i in range(len(pcd_roi.points)):
            tmp_point_3 = Point32()
            tmp_point_3.x = pcd_roi.points[i].x * cos(theta) + pcd_roi.points[i].y * -sin(theta) + self.ego.x
            tmp_point_3.y = pcd_roi.points[i].x * sin(theta) + pcd_roi.points[i].y * cos(theta) + self.ego.y
            pcd_coordi.points.append(tmp_point_3)
    
        self.pcd_pub.publish(pcd_roi)
        self.pcd_coordi_pub.publish(pcd_coordi)


if __name__ == '__main__':
    try:
        test=lidarParser()
    except rospy.ROSInterruptException:
        pass