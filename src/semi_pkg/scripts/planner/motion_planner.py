#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.motion import Motion
from .sub_function.find_local_path import findLocalPath
# from .sub_function.parking_diagonal import Parking_Motion
from .sub_function.parking_diagonal_LJY import Parking_Motion_LJY
from .sub_function.parking_parallel_hy import parallel_traj_hy

class MotionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.plan = parent.shared.plan
        self.ego = parent.shared.ego
        self.parking = parent.shared.park

        # self.trajectory = self.plan.trajectory # to controller
        self.global_path = self.shared.global_path  # from localizer

        # from global path (find_local_path)
        self.cut_path = self.shared.cut_path
        self.lattice_path = self.shared.lattice_path  # from LPP []

        self.motion = Motion(self.shared, self.plan, self.ego)
        #self.park_motion = Parking_Motion_LJY(self.shared, self.plan, self.ego)
        self.park_motion = parallel_traj_hy(self.shared, self.plan, self.ego,self.parking)
    def run(self):
        while True:
            try:
                findLocalPath(self.global_path, self.ego, self.cut_path)
                self.motion.path_maker()  # lattice_path

                if self.shared.plan.behavior_decision == "static_obstacle_avoidance":
                    self.motion.weight_function_obstacle_avoidance()
                    self.motion.select_trajectory()

                elif self.shared.plan.behavior_decision == "driving":
                    self.motion.lane_weight = self.motion.all_obstacle_aviodance()
                    self.motion.select_trajectory()
    

                elif self.shared.plan.behavior_decision == "emergency_avoidance":
                    self.motion.weight_function_AEB()
                    self.motion.select_trajectory()

                ################# parking ######################
                elif self.shared.plan.behavior_decision == "backward_trajectory_Create":
                    # self.park_motion.make_parking_tra()
                    #self.park_motion.making_backward_path()
                    self.park_motion.parking_back_phase2()
                
                elif self.shared.plan.behavior_decision == "forward_trajectory_Create":
                    # self.park_motion.make_parking_tra()
                    self.park_motion.making_forward_path()
                
                elif self.shared.plan.behavior_decision == "mamuri":
                    self.park_motion.manuri()
                
                elif self.shared.plan.behavior_decision == "exit":
                    self.park_motion.exit()

                elif self.shared.plan.behavior_decision == "forward_reverse_trajectory_Create":
                    # self.park_motion.make_parking_tra()
                    self.park_motion.making_reverse_forward_path()

                elif self.shared.plan.behavior_decision == "parkingForwardOn":
                    # self.park_motion.parking_drive(0)
                    self.motion.select_trajectory()

                elif self.shared.plan.behavior_decision == "parkingBackwardOn":
                    # self.park_motion.parking_drive(2)
                    self.motion.select_trajectory()
                
                
                    
                else:
                    pass
                #################################################

            except IndexError:
                print("++++++++motion_planner+++++++++")

            sleep(self.period)