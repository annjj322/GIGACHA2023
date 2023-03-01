#!/usr/bin/env python3
from re import A
import rospy
from math import sqrt
from time import time
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.mission import Mission
from std_msgs.msg import String
from planner_and_control.msg import Ego
from planner_and_control.msg import Perception
from planner_and_control.msg import Sign

class Behavior_Planner:
    def __init__(self):
        rospy.init_node('Behavior_Planner', anonymous = False)

        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/perception', Perception, self.perception_callback)
        rospy.Subscriber('/state', String, self.state_callback)

        self.pub_behavior = rospy.Publisher('/behavior', String, queue_size = 1)
        self.pub_ego = rospy.Publisher('/behavior_ego', Ego, queue_size = 1)

        self.ego = Ego()
        self.perception = Perception()
        self.state = String()

        self.behavior = " "
        self.sign_dis = 100
        self.traffic_dis = 100
        self.go_side_check = False
        self.sign_detected = 0 # action just one time
        self.mission = Mission(self.ego, self.perception)

    def ego_callback(self, msg):
        self.ego = msg

    def perception_callback(self, msg):
        self.perception = msg

    def state_callback(self, msg):
        self.state = msg.data

    def run(self):
        if self.state == "parking":
            self.mission.parking()
            
        elif self.state == "static_obstacle_detected":
            self.mission.static_obstacle(self.perception.objx, self.perception.objy, self.ego)
            
        elif self.state == "stop_sign_detected":
            self.mission.stop()

        elif self.state == "right_sign_detected":
            self.mission.turn_right()

        elif self.state == "left_sign_detected":
            self.mission.turn_left()
            
        elif self.state == "child_area":
            self.mission.child_area(self.perception.signx, self.perception.signy)

        elif self.state == "right_sign_area":
            self.mission.non_traffic_right


        else:
            self.mission.go()

        print(f"behavior_planner : {self.mission.behavior_decision}")
        print(f"speed : {self.mission.ego.target_speed}")

        self.pub_behavior.publish(self.mission.behavior_decision)
        self.pub_ego.publish(self.mission.ego)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    bp = Behavior_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        bp.run()
        rate.sleep
