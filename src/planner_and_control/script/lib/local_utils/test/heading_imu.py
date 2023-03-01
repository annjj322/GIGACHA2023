import rospy
import numpy as np
from planner_and_control.msg import Local

from sensor_msgs.msg import Imu

def imuCallback(data):
    imu_heading = data.heading

    
    print(imu_heading)

rospy.init_node('heading_imu', anonymous = False)
rospy.Subscriber("/pose", Local, imuCallback)
rospy.spin()

