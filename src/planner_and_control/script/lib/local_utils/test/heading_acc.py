import rospy
from ublox_msgs.msg import NavPVT

def gpsCallback(data):
    headAcc = data.headAcc * (10 ** (-5))

    print(headAcc)

rospy.init_node('heading_acc', anonymous = False)
rospy.Subscriber("/ublox_gps/navpvt", NavPVT, gpsCallback)
rospy.spin()