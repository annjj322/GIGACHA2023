from math import sqrt, hypot
from time import time, sleep
from math import cos, sin, pi, sqrt
from local_pkg.msg import Control_Info
import rospy
import numpy as np

class Behavior():
    def __init__(self, sh, eg, pc, pl):

        self.perception = pc
        self.shared = sh
        self.ego = eg
        self.plan = pl
        self.parking = self.shared.park

        self.global_path = self.shared.global_path

    def go(self):
        self.ego.target_estop = 0x00
        self.ego.target_gear = 0
        self.plan.motion_decision = "go"

    def parrallel_parking(self):
        if self.perception.parrallel_flag:
            self.plan.motion_decision = "parrallel_parking"
        else:
            self.plan.motion_decicion = "parrallel_parking"
            
    def diagonal_parking(self):
        if self.perception.diagonal_flag:
            self.plan.motion_decision = "diagonal_parking"
        else:
            self.plan.motion_decicion = "diagonal_parking"
        
    def delivery(self):
        if self.perception.delivery_flag:
            self.plan.motion_decision = "delivery"
        else:
            self.plan.motion_decision = "delivery"

    def obs(self):
        self.plan.motion_decision = "obs_tmp"