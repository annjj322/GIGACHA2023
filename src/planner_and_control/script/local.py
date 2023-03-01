#!/usr/bin/env python3
import rospy

from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Local
from lib.local_utils.gps import GPS
from lib.local_utils.heading import Heading

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)
        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        self.msg = Local()

        self.gps = GPS()
        self.heading = Heading()

    def main(self):
        if self.heading.headingAcc < 600000: # gps heading error less than 6 deg
            offset = self.heading.gps_heading - self.heading.imu_heading
            final_heading = self.heading.imu_heading + offset
            rospy.loginfo("Correction Heading : %f" %final_heading)
        else:
            final_heading = self.heading.imu_heading
            rospy.loginfo("AHRS Heading : %f" %final_heading)

        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.heading = final_heading

        self.pub.publish(self.msg)

        # rospy.loginfo("=========Localization=========")
        # rospy.loginfo("x : %f" %self.msg.x)
        # rospy.loginfo("y : %f" %self.msg.y)
        # rospy.loginfo("e2box_battery : %f" %self.heading.imu_battery)

if __name__ == '__main__':
    Activate_Signal_Interrupt_Handler()
    loc = Localization()
    rate = rospy.Rate(50)
 
    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()