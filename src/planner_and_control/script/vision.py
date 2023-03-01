#!/usr/bin/env python3
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Perception
        
class Vision:
    def __init__(self):
        rospy.init_node('Vision', anonymous = False)
        self.pub = rospy.Publisher("/vision", Perception, queue_size = 1)

        self.vision = Perception()
        self.vision.objx = []
        self.vision.objy = []
        self.vision.objr = []
        self.vision.signname = "go"

    def make_input(self):
        x = float(input("object x : "))
        y = float(input("object y : "))
        r = float(input("object r : "))

        self.vision.objx.append(x)
        self.vision.objy.append(y)
        self.vision.objr.append(r)
        
    def run(self):
        self.pub.publish(self.vision)
        self.make_input()
        self.vision.signname = "static_obstacle"

        print(f"x : {self.vision.objx}, y : {self.vision.objy}, r : {self.vision.objr}")

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    vi = Vision()
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        vi.run()
        rate.sleep
        