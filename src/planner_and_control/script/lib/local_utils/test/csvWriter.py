import csv
import rospy
from ublox_msgs.msg import NavPVT
import numpy as np
from planner_and_control.msg import Local
from sensor_msgs.msg import Imu


def imuCallback(data):
    imu_heading = data.heading % 360

    print(imu_heading)

# rospy.init_node('heading_imu', anonymous = False)


def gpsCallback(data):
    heading = data.heading
    gps_heading = (450 - (heading * 10**(-5))) % 360

    print(gps_heading)


data = [
    [imu_heading]
]

f = open("data2.csv", "w")
writer = csv.writer(f)

for row in data:
    writer.writerow(row)  # 여기 주목!

rospy.init_node('heading_gps', anonymous=False)
rospy.Subscriber("/pose", Local, imuCallback)
rospy.Subscriber("/ublox_gps/navpvt", NavPVT, gpsCallback)
rospy.spin()
