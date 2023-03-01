#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.motion import Motion
from .sub_function.find_local_path import findLocalPath
from .sub_function.parking_diagonal import Parking_Motion


class MotionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.plan = parent.shared.plan
        self.ego = parent.shared.ego
        # self.parking = parent.shared.parking

        # self.trajectory = self.plan.trajectory # to controller
        self.global_path = self.shared.global_path  # from localizer

        # from global path (find_local_path)
        self.cut_path = self.shared.cut_path
        self.lattice_path = self.shared.lattice_path  # from LPP []

        self.motion = Motion(self.shared, self.plan, self.ego)
        self.park_motion = Parking_Motion(self.shared, self.plan, self.ego)

    def run(self):
        while True:
            try:
                findLocalPath(self.global_path, self.ego, self.cut_path)
                self.motion.path_maker()  # lattice_path

                if self.shared.plan.behavior_decision == "static_obstacle_avoidance":
                    self.motion.weight_function_obstacle_avoidance()
                    self.motion.select_trajectory()

                elif self.shared.plan.behavior_decision == "driving":
                    self.motion.lane_weight = [10000, 1000, 0, 10000]
                    self.motion.select_trajectory()

                elif self.shared.plan.behavior_decision == "emergency_avoidance":
                    self.motion.weight_function_AEB()
                    self.motion.select_trajectory()

                ################# parking ######################
                elif self.shared.plan.behavior_decision == "parking_trajectory_Create":
                    self.park_motion.make_parking_tra()

                elif self.shared.plan.behavior_decision == "parkingForwardOn":
                    self.park_motion.parking_drive(0)

                elif self.shared.plan.behavior_decision == "parkingBackwardOn":
                    self.park_motion.parking_drive(2)
                    
                else:
                    pass
                #################################################

            except IndexError:
                print("++++++++motion_planner+++++++++")

            sleep(self.period)