import rospy
from ublox_msgs.msg import NavPVT

def gpsCallback(msg):
    hacc = msg.hAcc

    print(hacc)

rospy.init_node('gps_test', anonymous = False)
rospy.Subscriber("/ublox_gps/navpvt", NavPVT, gpsCallback)
rospy.spin()