import rospy 
import numpy as np 
from euler_from_quaternion import euler_from_quaternion as efq 
from sensor_msgs.msg import Imu 
 
def imuCallback(data): 
    orientation_q = data.orientation 
    roll, pitch, yaw = efq(orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w) 
 
    imu_heading = np.rad2deg(-1*yaw) 
 
    print(imu_heading) 
 
rospy.init_node('heading_raw', anonymous = False) 
rospy.Subscriber("/imu", Imu, imuCallback) 
rospy.spin()