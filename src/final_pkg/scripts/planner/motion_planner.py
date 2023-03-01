#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.motion import Motion
from .sub_function.find_local_path import findLocalPath
from .sub_function.parking_parallel import Parking_Motion

class MotionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.plan = parent.shared.plan
        self.ego = parent.shared.ego

        self.global_path = self.shared.global_path  # from localizer

        self.cut_path = self.shared.cut_path
        self.lattice_path = self.shared.lattice_path  # from LPP []

        self.lane_weight = [10000, 0, 10000]
        self.isObstacle = [1000, 1000, 1000]

        self.motion = Motion(self.shared, self.plan, self.ego)
        self.park_motion = Parking_Motion(self.shared, self.plan, self.ego)

    def run(self):
        while True:
            try:
                # from global path (50indexes)
                findLocalPath(self.global_path, self.ego, self.cut_path)
                self.motion.path_maker()  # lattice_path

                if self.shared.plan.behavior_decision == "static_obstacle_avoidance":
                    self.motion.weight_function_obstacle_avoidance()
                    self.motion.select_trajectory()

                elif self.shared.plan.behavior_decision == "turn_right":
                    pass

                elif self.shared.plan.behavior_decision == "turn_left":
                    pass

                elif self.shared.plan.behavior_decision == "driving":
                    self.motion.lane_weight = [10000, 0, 10000]
                    self.motion.select_trajectory()

                # parking
                elif self.shared.plan.behavior_decision == "parking_trajectory_Create":
                    self.park_motion.make_parking_tra()

                elif self.shared.plan.behavior_decision == "parkingForwardOn":
                    self.park_motion.parking_drive(0)

                elif self.shared.plan.behavior_decision == "parkingBackwardOn":
                    self.park_motion.parking_drive(2)

                ######################delivery###########################

                elif self.shared.plan.behavior_decision == "pickup_mode":
                    self.shared.selected_lane = 3

                elif self.shared.plan.behavior_decision == "pickup":
                    self.shared.selected_lane = 3
                
                elif self.shared.plan.behavior_decision == "pickup_end":
                    self.shared.selected_lane = 2

                elif self.shared.plan.behavior_decision == "delivery_mode":
                    self.shared.selected_lane = 4

                elif self.shared.plan.behavior_decision == "delivery":
                    self.shared.selected_lane = 4

                elif self.shared.plan.behavior_decision == "delivery_end":
                    self.shared.selected_lane = 1

                ######################delivery Siheung###########################

                # elif self.shared.plan.behavior_decision == "pickup":
                #     self.shared.selected_lane = 3
                
                # elif self.shared.plan.behavior_decision == "pickup_end":
                #     self.shared.selected_lane = 1

                # elif self.shared.plan.behavior_decision == "delivery":
                #     self.shared.selected_lane = 3

                # elif self.shared.plan.behavior_decision == "delivery_end":
                #     self.shared.selected_lane = 1

                else:
                    self.motion.select_trajectory()

            except IndexError:
                print("++++++++motion_planner+++++++++")

            sleep(self.period)