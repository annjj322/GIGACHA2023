# libarary
from filterpy.kalman import ExtendedKalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
import csv
import rospy
import time
from collections import deque 
# class
from ahrs import IMU
from gps import GPS
# msgs
from sensor_msgs.msg import Imu 
from local_pkg.msg import Local
from std_msgs.msg import Header
from geometry_msgs.msg import PointStamped
from sig_int_handler import Activate_Signal_Interrupt_Handler

class EKF() :
    def __init__ (self):
        rospy.init_node("EKF_GPS_IMU", anonymous=False)      
        self.pub = rospy.Publisher("/heading_ekf", PointStamped, queue_size=1)    
        #self.pub = rospy.Publisher("/heading_ekfs", PointStamped, queue_size=1)    
        rospy.Subscriber("/imu", Imu, self.imu_call_back)  
        rospy.Subscriber("/local_msgs", Local, self.gps_call_back)  
        
        # class
        self.imu = IMU()
        self.gps = GPS("Songdo")

        # ekf parameter
        dt = 0.001
        self.ekf = ExtendedKalmanFilter(dim_x=2, dim_z=2)
        self.ekf.x = np.array([[2], [0]]) # state estimate vector
        self.ekf.P = Q_discrete_white_noise(2,dt,0.5) # covariance matrix
        self.ekf.F = np.array([[1,dt],[0,1]]) # transition matrix # F * [yaw, r]k = [yaw, r]k+1 
        self.ekf.R = Q_discrete_white_noise(2,dt,1) # measurement noise matrix
        self.ekf.Q = Q_discrete_white_noise(2,dt,0.9) # process nosie matrix
        #self.ekf.H = np.array([[1, 0],[0, 1]]) # measurement matrix

        # EKF class's parameter
        self.r = 0.0
        self.yaw = 0.0
        self.gps_heading = 0.0
        self.heading_ekf = 0.0
        self.headAcc = 180.0
        self.gear = 0
        self.yaw_x = 0.0
        self.msg = PointStamped() 
        self.init = True

        self.count = 0
        self.offset =0 # None

        # moving filter
        self.deque_size = 35
        self.heading_data = deque(maxlen=self.deque_size)

        # imu_parameter
        self.imu_offset = 123+30-20

        self.heading = 0

    def imu_call_back(self,data):
        self.r = data.angular_velocity.z       

    # def gps_call_back(self,data):
    #     self.gps_heading = data.gps_heading
    #     # print("headACC : ", data.headAcc)
    #     self.headAcc = data.headAcc
    #     self.yaw = (data.imu_heading) %360
    #     self.gear = data.gear

    def gps_call_back(self,data):
        self.gps_heading = data.gps_heading
        # print("headACC : ", data.headAcc)
        self.headAcc = data.headAcc
        self.yaw = (data.imu_heading - self.imu_offset) %360

        self.gear = data.gear
        #if self.gear == 0:
        #    self.heading = self.yaw
        #    print("heading : ", self.heading)
        #else:
        #    self.heading = (self.yaw+180)%360
        #    print("backward heading : ", self.heading)

    def HJacobian(self,x):
        H= np.array([[1, 0.001],[0, 1]])
        return H 

    def moving_average_filter(self,heading):      
        

        self.heading_data.append(heading)

        if len(self.heading_data) == self.deque_size:
            filtered_data = np.mean(self.heading_data)           
        
        else :
            filtered_data = heading
        
        return self.heading_data, filtered_data

    def Hx(self,x,H):
        return H @ x       
    
    def main(self):  
        
        
        if self.init and self.gear == 0:
            if self.headAcc <= 10:         
                self.init = False
                self.offset = self.gps_heading - self.yaw                        
                self.yaw_x = (self.yaw + self.offset)%360              
           

        if self.gear == 0 :       
            if self.headAcc <= 2:         
                self.offset = self.gps_heading - self.yaw                        
            self.yaw_x = (self.yaw + self.offset)%360    

            if self.headAcc >= 2 : 
                self.ekf.R = np.eye(2)*120 *self.headAcc
                self.ekf.P = np.eye(2)*0.5 *self.headAcc            
            else :
                self.ekf.R = np.eye(2) * self.headAcc * 50
                self.ekf.P = np.eye(2) * self.headAcc *0.5
                
            
            
        else :  # 후진
            if self.headAcc <= 2:         
                gps_back = (self.gps_heading-180)%360                
                self.offset = gps_back - self.yaw
            gps_back = (self.gps_heading-180)%360 # jm
            self.offset = gps_back - self.yaw # jm
            self.yaw_x = (self.yaw + self.offset)% 360

            self.ekf.R = np.eye(2)*120 *self.headAcc
            self.ekf.P = np.eye(2)*0.5 *self.headAcc  

        z = [[self.gps_heading],[self.r]]        
        self.ekf.x = [[self.yaw_x],[self.r]]

        
        H = np.array([[1, 0],[0, 1]])
        self.ekf.predict_update(z,self.HJacobian, self.Hx,hx_args=H) 
        self.heading_ekf = self.ekf.x[0][0]    

        #self.heading = self.heading_ekf
        heading_data, self.heading = self.moving_average_filter(self.heading_ekf)
        
        # rosmsg
        self.msg.header = Header()                
        self.msg.header.stamp = rospy.Time.now()
        self.msg.header.frame_id = "heading_EKF"

        
        self.msg.point.x = self.heading % 360 #(self.heading_ekf) % 360
        self.msg.point.y = self.gps_heading
        self.msg.point.z = self.yaw_x # self.yaw

        self.pub.publish(self.msg)
        rospy.loginfo(self.msg)   



if __name__ == '__main__': 
    Activate_Signal_Interrupt_Handler()  
    ekf = EKF()
    rate = rospy.Rate(1000)
    while not rospy.is_shutdown():        
        ekf.main()
        rate.sleep()
    