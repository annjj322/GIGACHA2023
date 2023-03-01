#!/usr/bin/env python3
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Local, Serial_Info, Perception, Ego
from lib.planner_utils.index_finder import IndexFinder
import rospy

class Ego_updater:
    def __init__(self):
        rospy.init_node('Ego', anonymous = False)
        self.ego_pub = rospy.Publisher("/ego", Ego, queue_size = 1)

        rospy.Subscriber("/pose", Local, self.local_callback) # local
        rospy.Subscriber("/behavior_ego", Ego, self.behavior_callback) 
        rospy.Subscriber("/serial", Serial_Info, self.serial_callback) # serial

        self.ego = Ego()

        self.ego.map_folder = input("folder name : ")

        if self.ego.map_folder == "1":
            self.ego.map_folder = "songdo_track/maps"
            self.ego.map_file = "songdo_straight"
        elif self.ego.map_folder == "2":
            self.ego.map_folder = "kcity_simul"
            self.ego.map_file = "ex"
        elif self.ego.map_folder == "3":
            self.ego.map_folder = "kcity_simul/turn_right"
            self.ego.map_file = "turn_right"
        elif self.ego.map_folder == "4":
            self.ego.map_folder = "kcity_simul"
            self.ego.map_file = "kcity_straight_lane!"

        self.IF = IndexFinder(self.ego)

    def local_callback(self, msg):
        self.ego.x = msg.x
        self.ego.y = msg.y
        self.ego.heading = msg.heading

    def behavior_callback(self, msg):
        self.ego.target_speed = msg.target_speed
        self.ego.target_brake = msg.target_brake
        self.ego.target_gear = msg.target_gear

    def serial_callback(self, msg):
        self.ego.speed = msg.speed
        self.ego.steer = msg.steer
        self.ego.brake = msg.brake
        self.ego.gear = msg.gear
        self.ego.auto_manual = msg.auto_manual

    def run(self):
        self.ego.index = self.IF.run()
        self.ego_pub.publish(self.ego)
        rospy.loginfo(self.ego)

        print("Ego updater is operating")

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    eg = Ego_updater()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        eg.run()
        rate.sleep()
        
