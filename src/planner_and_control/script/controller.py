#!/usr/bin/env python3

# from planner_and_control.script.lib.controller_utils.stanley import Stanley
from lib.controller_utils.stanley import Stanley
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.controller_utils.pure_pursuit import PurePursuit
from lib.controller_utils.pid import PID
from std_msgs.msg import String
from planner_and_control.msg import Path, Control_Info, Ego, Parking

from time import sleep

class LocalPath:
    def __init__(self):
        self.data = Path()


class ControlEgo:
    def __init__(self):
        self.data = Ego()


class Controller:
    def __init__(self):
        rospy.init_node('Controller', anonymous=False)
        rospy.Subscriber('/trajectory', Path, self.motion_callback)
        
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/parking', Parking, self.parking_call_back)
        self.control_pub = rospy.Publisher(
            '/controller', Control_Info, queue_size=1)
        self.control_msg = Control_Info()

        self.parking = Parking()
        self.ego = ControlEgo()
        self.trajectory = LocalPath()  # add motion trajectory
        self.target_speed = 5.0
        self.ego.speed = 5.0
        self.ego.target_speed = 4.9
        self.ego.auto_manual = 0

        self.lat_controller = PurePursuit(self.ego, self.trajectory, self.parking)
        self.lat_controller = Stanley(self.ego, self.trajectory, self.parking)
        # self.lon_controller = PID(self.ego)

    def motion_callback(self, msg):
        self.trajectory.data = msg
        

    def ego_callback(self, msg):
        self.ego.data = msg

    def parking_call_back(self, msg):
        self.parking.index = msg.index
        self.parking.on = msg.on

    def run(self):
        if len(self.trajectory.data.x) == 0:
            self.publish_control_info(1, 0)
        else:
            self.publish_control_info(0, 0)
        self.target_speed = 2.5
        # print("Controller On..")

    def publish_control_info(self, estop, gear):
        self.control_msg.emergency_stop = estop
        self.control_msg.gear = gear
        try:
            self.control_msg.steer = self.lat_controller.run()
        except IndexError:
            print("index Error")
        # a = list(self.trajectory.data.x)
        # print(f"trajectory : {a[0]}")
        # if self.ego.speed > self.ego.target_speed:
        #     self.control_msg.speed = self.lon_controller.decel()
        # else:
        #     self.control_msg.speed = self.ego.data.target_speed
        self.control_msg.speed = self.ego.data.target_speed

        self.control_msg.brake = 0  # PID on
        # self.control_msg.speed, self.control_msg.brake = self.ego.data.target_speed, 0               ## PID off
        self.control_pub.publish(self.control_msg)


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    cc = Controller()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        cc.run()
        rate.sleep()
