import rospy
from ublox_msgs.msg import NavPVT

def gpsCallback(data):
    heading = data.heading
    gps_heading = (450 - (heading * 10**(-5))) % 360

    print(gps_heading)


rospy.init_node('heading_gps', anonymous = False)
rospy.Subscriber("/ublox_gps/navpvt", NavPVT, gpsCallback)
rospy.spin()