#!/usr/bin/env python3
import rospy
from math import sqrt
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Perception
from planner_and_control.msg import Ego
from planner_and_control.msg import Path
from planner_and_control.msg import Sign
from sensor_msgs.msg import PointCloud

class Mission_Planner:
    def __init__(self):
        rospy.init_node('Mission_Planner', anonymous = False)
        
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/perception', Perception, self.perception_callback)

        self.pub = rospy.Publisher('/state', String, queue_size = 1)

        self.ego = Ego()
        self.perception = Perception()
        self.state = ''
        self.obs_dis = 100
        self.sign = ''
        self.sign_dis = 100

    def perception_callback(self, msg):
        self.perception = msg

    def ego_callback(self, msg):
        self.ego = msg

    def run(self):

        if self.perception.signname == "turn_right_traffic_light":
            self.state = "right_sign_detected"

        elif self.perception.signname == "static_obstacle":
            self.state = "static_obstacle_detected"           

        elif self.perception.signname == "delivery":
            self.state = "stop_sign_detected"

        elif self.perception.signname == "child_area":
            self.state = "child_area"
        
        elif self.perception.signname == "turn_left_traffic_light":
            self.state = "left_sign_detected"

        elif self.perception.signname == "non_traffic_right":
            self.state ="right_sign_area"

        else:
            self.state = "go"
        print(f"mission_planner : {self.state}")
        self.pub.publish(self.state)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mm = Mission_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mm.run()
        rate.sleep()
