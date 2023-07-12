#!/usr/bin/env python3
import threading
from time import sleep
# from .sub_function.motion import Motion
from .sub_function.motion_morai import Motion
# from .sub_function.parking_diagonal import Parking_Motion
# from .sub_function.parking_diagonal_LJY import Parking_Motion_LJY
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

        self.motion = Motion(self.shared, self.plan, self.ego)
        # self.park_motion = Parking_Motion_LJY(self.shared, self.plan, self.ego) # 캡스톤
        self.park_motion = parallel_traj_hy(self.shared, self.plan, self.ego,self.parking)

    def run(self):
        while True:
            try:
                if self.shared.plan.behavior_decision == "go":
                    pass
                
                elif self.shared.plan.behavior_decision == "parking":
                    pass
                # ################ parking ######################
                elif self.shared.plan.behavior_decision == "backward_trajectory_Create":
                    # self.park_motion.make_parking_tra()
                    # self.park_motion.making_backward_path()
                    pass
                
                elif self.shared.plan.behavior_decision == "forward_trajectory_Create":
                    # self.park_motion.make_parking_tra()
                    self.park_motion.making_forward_path()

                elif self.shared.plan.behavior_decision == "forward_reverse_trajectory_Create":
                    # self.park_motion.make_parking_tra()
                    self.park_motion.making_reverse_forward_path()
                ###########################################################################
                elif self.shared.plan.behavior_decision == "forward_trajectory_Create_para":
                    self.park_motion.making_forward_path()
                
                elif self.shared.plan.behavior_decision == "exit":
                    self.park_motion.exit()
                elif self.shared.plan.behavior_decision == "backward_trajectory_Create_para":
                    self.park_motion.backward_path()
                #################공통#############################################    
                elif self.shared.plan.behavior_decision == "parkingForwardOn":
                    pass
                elif self.shared.plan.behavior_decision == "parkingBackwardOn":
                    pass
                
                    
                else:
                    pass
                #################################################

            except IndexError:
                print("++++++++motion_planner+++++++++")

            sleep(self.period)