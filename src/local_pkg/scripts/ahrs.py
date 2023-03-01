import rospy 
import numpy as np 
import time 
from geometry_msgs.msg import Pose 
from local_functions import euler_from_quaternion as efq 
from sensor_msgs.msg import Imu 
from geometry_msgs.msg import Quaternion 
 
class IMU(): 
    def __init__(self): 
        rospy.Subscriber("/imu", Imu, self.imu_call_back) 
        rospy.Subscriber("/simul_imu", Pose, self.imu_call_back_simul) 

        self.roll = 0.0 
        self.pitch = 0.0 
        self.heading = 0.0 
 
        self.battery = 0 
        self.time = 0.0 
 
        self.linear_accel_x = 0.0 
        self.linear_accel_y = 0.0 
        self.angular_velocity_z = 0.0 
         
        self.orientation_q = Quaternion() 
 
    def imu_call_back(self, data):
        self.time = time.time() 
        self.orientation_q = data.orientation 
        roll, pitch, yaw = efq(self.orientation_q.x, self.orientation_q.y, self.orientation_q.z, self.orientation_q.w) 
         
        self.roll = roll 
        self.pitch = pitch 
 
        self.heading = np.rad2deg(-1*yaw)%360
        self.battery = data.linear_acceleration.z 

    def imu_call_back_simul(self, data):
        self.time = time.time() 
        self.orientation_q = data.orientation 
        roll, pitch, yaw = efq(self.orientation_q.x, self.orientation_q.y, self.orientation_q.z, self.orientation_q.w) 
         
        self.roll = roll 
        self.pitch = pitch 

        self.heading = np.rad2deg(yaw)%360
 
 
if __name__ == '__main__': 
    try: 
        imu=IMU()
        rospy.spin()
    except rospy.ROSInterruptException: 
        pass