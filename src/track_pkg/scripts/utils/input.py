#!/usr/bin/env python3
import rospy
from sig_int_handler import ActivateSignalInterruptHandler
from planner_and_control.msg import Perception

class Input:
    def __init__(self):
        rospy.init_node('Input', anonymous = False)
        self.pub = rospy.Publisher("/input", Perception, queue_size = 1)
        self.perception = Perception()
        self.perception.objx = []
        self.perception.objy = []
        self.perception.objr = [1]
        
    def run(self):
        for i in range(3):
            self.perception.objx = [i+1]
            self.perception.objy = [i+3]
            print(self.perception.objx[0])
            print(self.perception.objy[0])
            self.pub.publish(self.perception)
            rate.sleep()

if __name__ == "__main__":
    ActivateSignalInterruptHandler()
    ss = Input()
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep()