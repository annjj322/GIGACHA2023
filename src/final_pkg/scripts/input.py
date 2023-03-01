#!/usr/bin/env python3

import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Perception

class Input:
    def __init__(self):
        rospy.init_node('Input', anonymous = False)
        self.pub = rospy.Publisher("/input", Perception, queue_size = 1)

        self.perception = Perception()

        self.perception.A_target = 0
        self.perception.A_objx = 0.0
        self.perception.A_objy = 0.0

        self.perception.bbox_size = []
        self.perception.B_target_x = []
        self.perception.B_target_y = []

        for i in range (3):
            self.perception.bbox_size.append(0)
            self.perception.B_target_x.append(0.0)
            self.perception.B_target_y.append(0.0)

        self.perception.signname = ""

    def function(self):
        self.perception.A_target = int(input("A_target : "))
        self.perception.A_objx = float(input("A_objx : "))
        self.perception.A_objy = float(input("A_objy : "))
        self.perception.bbox_size[0], self.perception.bbox_size[1], self.perception.bbox_size[2] = map(int, input("bbox_size = ").split())
        self.perception.B_target_x[0], self.perception.B_target_x[1], self.perception.B_target_x[2] = map(float, input("B_target_x = ").split())
        self.perception.B_target_y[0], self.perception.B_target_y[1], self.perception.B_target_y[2] = map(float, input("B_target_y = ").split())
        self.perception.signname = "delivery"
        
    def run(self):
        self.pub.publish(self.perception)
        print("input_mission : ", self.perception.signname)
        
if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    ss = Input()
    rate = rospy.Rate(1)
    ss.function()
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep()