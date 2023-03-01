#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from math import sqrt
import rospy
from geometry_msgs.msg import Point, PoseArray
from visualization_msgs.msg import MarkerArray, Marker
from sensor_msgs.msg import PointCloud 
import itertools as it
import numpy as np

class path_maker:
    def __init__(self):
        # make node
        rospy.init_node("narrow_path_maker", anonymous=False)

        #subscriber
        #rospy.Subscriber("obstacles_markers", MarkerArray, self.makePath)
        rospy.Subscriber('/cone_info', PoseArray, self.makePath)
    
        # publisher
        self.pub = rospy.Publisher('target_point', Point, queue_size=10)
        self.vis_pub = rospy.Publisher('target_point_vis', Marker, queue_size=10)

        # lookahead point
        self.left_obs = []
        self.right_obs = []
        #self.obstacles = []
        self.nearest_obstacles = []
        
        self.target_point = Point()
        # visualize용 메세지
        # self.target_point_vis = Marker()

        rospy.spin()

    def calc_distance(self, obs_x, obs_y):
        p1 = [0, 0]
        p2 = [obs_x, obs_y]
        dis = sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p1, p2)))
        return dis

    def makeVisual(self):
        vis_target_marker = Marker()
        vis_target_marker.header.frame_id = "map"
        vis_target_marker.header.stamp = rospy.Time()
        vis_target_marker.ns = "circles"
        vis_target_marker.id = 0
        vis_target_marker.type = Marker.CYLINDER
        vis_target_marker.action = Marker.ADD
        vis_target_marker.pose.position.x = self.target_point.x
        vis_target_marker.pose.position.y = self.target_point.y
        vis_target_marker.pose.position.z = 0
        vis_target_marker.pose.orientation.x = 0.0
        vis_target_marker.pose.orientation.y = 0.0
        vis_target_marker.pose.orientation.z = 0.0
        vis_target_marker.pose.orientation.w = 1.0
        vis_target_marker.scale.x = 1
        vis_target_marker.scale.y = 1
        vis_target_marker.scale.z = 0.1
        vis_target_marker.color.r = 255
        vis_target_marker.color.g = 0
        vis_target_marker.color.b = 0
        vis_target_marker.color.a = 0.7
        vis_target_marker.lifetime = rospy.Duration(0.1)
        self.vis_pub.publish(vis_target_marker)
    
    #인지로 부터 받아온 센서퓨전된 러버콘을 좌측 러버콘과 우측러버콘으로 분리하여 리턴한다.
    def left_right_classification(self, points):
        tmp_left_obs = []
        tmp_right_obs = []
        for point in points:
            if point[3] == 0:
                tmp_left_obs.append(point)
            elif point[3] == 1:
                tmp_right_obs.append(point)
        return (tmp_left_obs, tmp_right_obs)


    #해당 코드는 인지된 러버콘이 2개일때 실행된다. 이때 좌측이나 우측에만 2개가 인지되는 부분을 분기문으로 pass시켜주었다.
    #좌측과 우측에 1개씩 인지되는 부분을 중점좌표로 target_point를 생성시켜주었다.
    def secondCOM(self, left_points, right_points):
        
        if len(left_points) == 2 or len(right_points) == 2:
            pass
        else:
            self.target_point.x = (left_points[0][0] + right_points[0][0]) / 2
            self.target_point.y = (left_points[0][1] + right_points[0][1]) / 2

    #해당 코드는 인지된 러버콘이 3개혹은 4개일때 실행된다. 저번과 달라진점은 ego의 상대좌표 (0,0)을 원의 중점을 생성하기 위한 point에 추가해주었다.
    def cal_circul(self, left_points, right_points):

        x_list=[]
        y_list=[]
        points=[[0, 0, 0, 0]]

        for point in left_points:
            points.append(point)

        for point in right_points:
            points.append(point)

        for point in points:
            x = point[0]
            y = point[1]
            x_list.append([-2*x,-2*y,1])
            y_list.append(-(x*x)-(y*y))
        
        #print(points)
        x_matrix=np.array(x_list)
        y_matrix=np.array(y_list)
        x_trans=x_matrix.T
            
        a_matrix=np.linalg.inv(x_trans.dot(x_matrix)).dot(x_trans).dot(y_matrix)
        a=a_matrix[0]
        b=a_matrix[1]
        c=a_matrix[2]
        r=sqrt(a*a+b*b-c)

        #아쉬운점은 여기에 딱 하나 rules based가 추가되었는데 이유는 r이 5보다 클 경우 gui상에서 직선 구간임이 자명하지만 이를 pass로 처리해주지 않으면 원의 중점이
        #코스 밖에 생성되기도 하기에 이를 방지하기 위한 rules_based이다.
        if r>5:
            print("r>5",r)

        else:
            print("r<5",r)
            self.target_point.x = a
            self.target_point.y = b


    def makePath(self, msg):
        obstacles=[]
        
        for point in msg.poses:
            tmp_obs_dis = self.calc_distance(point.orientation.x, point.orientation.y)
            obstacles.append([round(point.orientation.x, 2), round(point.orientation.y, 2), round(tmp_obs_dis, 2), point.orientation.w]) # x좌표,y좌표,거리좌표,객체id(0==y, 1==b)
        
        #print("self.obstacles : ", obstacles)

        self.left_obs,self.right_obs=self.left_right_classification(obstacles) #separate left_cone, right_cone
        # 점 정렬 & 왼쪽2개 오른쪽2개 필터링
        self.left_obs.sort(key = lambda x : x[2])
        self.right_obs.sort(key= lambda x : x[2])

        # 왼쪽에서 인식한 러버콘수가 2개초과이면 2개만 남긴다
        # 그 뒤 오른쪽에서 인식한 러버콘 수가 2개 초과이면 2개만 남긴다.
        # 위의 분기문을 다 거치고 나면 왼쪽 오른쪽 전부 2개 이하만 남음 (2,2),(2,1),(1,2),(1,1),(1,0),(0,1),(0,0)
        # 해당 러버콘 수에 따라 분기문을 나눈다. -> 0개 1개일땐 pass, 2개 일땐 secondCOM, 3개,4개 일땐 cal_circul 사용

        # print(self.left_obs[0][0])
        if len(self.left_obs) > 2:
            self.left_obs = self.left_obs[0:2]   

        if len(self.right_obs) > 2:
            self.right_obs=self.right_obs[0:2]

        #print("self.left_obs : ",self.left_obs)
        #print("self.right_obs : ",self.right_obs)

        if len(self.left_obs)+len(self.right_obs) == 0:
            pass
        elif len(self.left_obs)+len(self.right_obs) == 1:
            pass
        elif len(self.left_obs)+len(self.right_obs) == 2:
            self.secondCOM(self.left_obs, self.right_obs)
        elif len(self.left_obs)+len(self.right_obs) == 3:
            self.cal_circul(self.left_obs, self.right_obs)
        else:
            self.cal_circul(self.left_obs, self.right_obs)

        # print("self.obstacles",obstacles)
   
        self.makeVisual()
        self.pub.publish(self.target_point)

        #rospy.sleep(0.36) #default 0.1
        

if __name__ == "__main__":
   #print("PATH_MAKER_ON")
    path_maker()
