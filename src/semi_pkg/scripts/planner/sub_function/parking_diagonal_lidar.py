#!/usr/bin/env python3 

import pymap3d
import rospy 
import json

from math import cos, sin, pi

from sensor_msgs import point_cloud2 
from sensor_msgs.msg import PointCloud2, PointCloud, ChannelFloat32 
from geometry_msgs.msg import PolygonStamped, Point32
from std_msgs.msg import Int32
 
import numpy as np 
from shapely.geometry import Point, Polygon 

class PL():
    def __init__(self, ego):

        self.ego = ego
        rospy.Subscriber("/velodyne_points", PointCloud2, self.getMsg_parking) 
        self.pub = rospy.Publisher("lidar_pub", PointCloud, queue_size=1) 
        self.pub_num = rospy.Publisher("Parking_num", Int32, queue_size=1) 
        self.pub_roi1 = rospy.Publisher("Parking_ROI1", PolygonStamped, queue_size=1)
        self.pub_roi2 = rospy.Publisher("Parking_ROI2", PolygonStamped, queue_size=1) 
        self.pub_roi3 = rospy.Publisher("Parking_ROI3", PolygonStamped, queue_size=1) 
        self.pub_roi4 = rospy.Publisher("Parking_ROI4", PolygonStamped, queue_size=1) 
        self.pub_roi5 = rospy.Publisher("Parking_ROI5", PolygonStamped, queue_size=1) 
        self.pub_roi6 = rospy.Publisher("Parking_ROI6", PolygonStamped, queue_size=1) 

        # simul kcity
        self.base_lat = 37.23873
        self.base_lon = 126.772383333333
        self.base_alt = 15.4
        with open('/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/planner/sub_function/parking_JSON/parking_KCity_diagonal_roi2.json') as pkc:
            self.parking_point = json.load(pkc)

        parking_point_x_y = []

        for i in range(1, 7):
            self.point = self.parking_point[str(i)]
            for j in range(1, 5):
                x1 = self.point[str(j)][0]
                y1 = self.point[str(j)][1]
                x, y, _ = pymap3d.geodetic2enu(x1, y1, self.base_alt, self.base_lat, self.base_lon, self.base_alt)
                parking_point_x_y.append([x, y])
        
        # K-City
        # parking_point_x_y = [[9.021042, 9.433509],[8.873212, 12.023061],[10.647854, 12.023063],[10.352018, 14.612615],[11.978832, 14.612617],[11.830912, 17.202281],[13.309809, 17.202283],[13.161889, 19.791835],[14.640786, 19.791837],[14.492865, 22.381390],[15.971761, 22.566400],[15.823840, 24.971055],[20.709098, 25.340970],[20.556188, 22.751418],[19.225208, 22.751414],[19.373130, 20.161751],[17.894234, 20.161748],[17.894239, 17.572196],[16.563259, 17.387185],[16.563263, 14.982641],[15.084455, 14.797630],[15.232287, 12.392975],[13.753477, 12.392972],[13.901309, 9.803420]] 
        # Siheung 
        # parking_point_x_y = [[82.1174400754127, 76.6507403208519],[80.0800082015908, 76.4509484464359],[82.9236038219563, 71.7452329727534],[80.7178620986089, 71.4233563178608],[11.978832, 14.612617],[11.830912, 17.202281],[13.309809, 17.202283],[13.161889, 19.791835],[14.640786, 19.791837],[14.492865, 22.381390],[15.971761, 22.566400],[15.823840, 24.971055],[20.709098, 25.340970],[20.556188, 22.751418],[19.225208, 22.751414],[19.373130, 20.161751],[17.894234, 20.161748],[17.894239, 17.572196],[16.563259, 17.387185],[16.563263, 14.982641],[15.084455, 14.797630],[15.232287, 12.392975],[13.753477, 12.392972],[13.901309, 9.803420]] 
        # K-City_SangUk
        # parking_point_x_y = [[79.1993047047795,70.27442684757285],[79.50101764967633,67.75512916410418],[],[][80.54800691671798,72.93801733707124],[80.77873449928563,70.4187190083911],[85.35728223391854,73.17112786906065],[85.37505266803925,70.80720286915854][83.54710123154369,77.89896006004295],[83.48501033013567,75.73480257073666],[88.06355556288804,78.3651322843777],[88.10794717039578,75.92351986733988],[82.02093420200158,75.49062686278752],[82.08307080706561,73.01571987703883],[86.59950542236862,75.65714641458624],[86.8124863825727,73.32651814473104],[84.72721007747671,80.56254957593879],[84.92244601195848,78.03215273434014],[89.35901577777751,80.90664301860244],[89.18157691797795,78.54271592381856]]
        parking_space_1 = [parking_point_x_y[0], parking_point_x_y[1], parking_point_x_y[2], parking_point_x_y[3]] 
        parking_space_2 = [parking_point_x_y[4], parking_point_x_y[5], parking_point_x_y[6], parking_point_x_y[7]] 
        parking_space_3 = [parking_point_x_y[8], parking_point_x_y[9], parking_point_x_y[10], parking_point_x_y[11]] 
        parking_space_4 = [parking_point_x_y[12], parking_point_x_y[13], parking_point_x_y[14], parking_point_x_y[15]] 
        parking_space_5 = [parking_point_x_y[16], parking_point_x_y[16], parking_point_x_y[18], parking_point_x_y[19]] 
        parking_space_6 = [parking_point_x_y[20], parking_point_x_y[21], parking_point_x_y[22], parking_point_x_y[23]] 

        # 직사각형 생성 
        self.parking_space_poly1 = Polygon(parking_space_1) 
        self.parking_space_poly2 = Polygon(parking_space_2) 
        self.parking_space_poly3 = Polygon(parking_space_3) 
        self.parking_space_poly4 = Polygon(parking_space_4) 
        self.parking_space_poly5 = Polygon(parking_space_5) 
        self.parking_space_poly6 = Polygon(parking_space_6) 
        
        p1, p2, p3, p4, p5, p6 = PolygonStamped(), PolygonStamped(), PolygonStamped(), PolygonStamped(), PolygonStamped(), PolygonStamped()
        p1.header.frame_id, p2.header.frame_id, p3.header.frame_id, p4.header.frame_id, p5.header.frame_id, p6.header.frame_id = "map", "map", "map", "map", "map", "map"
        p1.header.stamp, p2.header.stamp, p3.header.stamp, p4.header.stamp, p5.header.stamp, p6.header.stamp = rospy.Time.now(), rospy.Time.now(), rospy.Time.now(), rospy.Time.now(), rospy.Time.now(), rospy.Time.now()
        
        p1.polygon.points = [Point32(x = parking_point_x_y[0][0], y = parking_point_x_y[0][1]),
                        Point32(x = parking_point_x_y[1][0], y = parking_point_x_y[1][1]),
                        Point32(x = parking_point_x_y[2][0], y = parking_point_x_y[2][1]),
                        Point32(x = parking_point_x_y[3][0], y = parking_point_x_y[3][1])]
        
        p2.polygon.points = [Point32(x = parking_point_x_y[4][0], y = parking_point_x_y[4][1]),
                        Point32(x = parking_point_x_y[5][0], y = parking_point_x_y[5][1]),
                        Point32(x = parking_point_x_y[6][0], y = parking_point_x_y[6][1]),
                        Point32(x = parking_point_x_y[7][0], y = parking_point_x_y[7][1])]
        
        p3.polygon.points = [Point32(x = parking_point_x_y[8][0], y = parking_point_x_y[8][1]),
                        Point32(x = parking_point_x_y[9][0], y = parking_point_x_y[9][1]),
                        Point32(x = parking_point_x_y[10][0], y = parking_point_x_y[10][1]),
                        Point32(x = parking_point_x_y[11][0], y = parking_point_x_y[11][1])]
        
        p4.polygon.points = [Point32(x = parking_point_x_y[12][0], y = parking_point_x_y[12][1]),
                        Point32(x = parking_point_x_y[13][0], y = parking_point_x_y[13][1]),
                        Point32(x = parking_point_x_y[14][0], y = parking_point_x_y[14][1]),
                        Point32(x = parking_point_x_y[15][0], y = parking_point_x_y[15][1])]
        
        p5.polygon.points = [Point32(x = parking_point_x_y[16][0], y = parking_point_x_y[16][1]),
                        Point32(x = parking_point_x_y[17][0], y = parking_point_x_y[17][1]),
                        Point32(x = parking_point_x_y[18][0], y = parking_point_x_y[18][1]),
                        Point32(x = parking_point_x_y[19][0], y = parking_point_x_y[19][1])]
        
        p6.polygon.points = [Point32(x = parking_point_x_y[20][0], y = parking_point_x_y[20][1]),
                        Point32(x = parking_point_x_y[21][0], y = parking_point_x_y[21][1]),
                        Point32(x = parking_point_x_y[22][0], y = parking_point_x_y[22][1]),
                        Point32(x = parking_point_x_y[23][0], y = parking_point_x_y[23][1])]

        self.pub_roi1.publish(p1)
        self.pub_roi2.publish(p2)
        self.pub_roi3.publish(p3)
        self.pub_roi4.publish(p4)
        self.pub_roi5.publish(p5)
        self.pub_roi6.publish(p6)


    def parking(self, temp_points):
    
        parking_result = [0, 0, 0, 0, 0, 0] 
        
        for i in range(len(temp_points)): 
            test_code = Point(temp_points[i].x, temp_points[i].y) 
            if test_code.within(self.parking_space_poly1): 
                parking_result[0]+=1 
            if test_code.within(self.parking_space_poly2): 
                parking_result[1]+=1 
            if test_code.within(self.parking_space_poly3): 
                parking_result[2]+=1 
            if test_code.within(self.parking_space_poly4): 
                parking_result[3]+=1 
            if test_code.within(self.parking_space_poly5): 
                parking_result[4]+=1 
            if test_code.within(self.parking_space_poly6): 
                parking_result[5]+=1 
    
        # print("parking 1 :", parking_result[0])  
        # print("parking 2 :", parking_result[1]) 
        # print("parking 3 :", parking_result[2]) 
        # print("parking 4 :", parking_result[3]) 
        # print("parking 5 :", parking_result[4]) 
        # print("parking 6 :", parking_result[5]) 
        
        # diagonal
        result_number = -1 
        if 720 <= self.ego.index < 805:
            for i in range(0, 2): 
                if parking_result[i] < 5:
                    result_number = i + 1 
                    break

        elif 808 <= self.ego.index <= 855:
            for i in range(2, 4): 
                if parking_result[i] < 5: 
                    result_number = i + 1 
                    break

        elif 866 <= self.ego.index <= 916:
            for i in range(4, 6): 
                if parking_result[i] < 5: 
                    result_number = i + 1 
                    break
                    
        # print(result_number)
        return result_number
 
    def getMsg_parking(self, lidar_data): 
        gen = point_cloud2.read_points(lidar_data, skip_nans=True) 
        cnt = 0 
        points_list = [] 
    
        for p in gen: 
            if (0 < p[0] < 20) and (-15 < p[1] < 0) and (-0.5 < p[2]): 
                points_list.append([p[0] + 1.15, p[1]]) 
    
        test = PointCloud() 
        # get_in = ChannelFloat32() 
        # get_in.name = 'VLP_intensery' 
        test.points = [] 
        theta = self.ego.heading * pi / 180 
        for p in points_list: 
            park = Point32() 
            park.x = p[0] * cos(theta) + p[1] * -sin(theta) + self.ego.x
            park.y = p[0] * sin(theta) + p[1] * cos(theta) + self.ego.y
            park.z = 0 
            # get_in.values.append(p[3]) 
            test.points.append(park) 
            cnt += 1 
    
        parking_number = Int32() 
        # print(type(test.points)) 
        parking_number.data = self.parking(test.points) 
        self.pub_num.publish(parking_number) 
        # print('===================================================parking number published', parking_number) 
    
        # print("Input :", cnt) 
        # test.channels.append(get_in) 
        test.header.frame_id = 'map' 
        test.header.stamp = rospy.Time.now() 
        self.pub.publish(test)