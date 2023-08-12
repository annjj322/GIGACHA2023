#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.motion import Motion, Potential_field
class MotionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.plan = parent.shared.plan
        self.ego = parent.shared.ego
        self.parking = parent.shared.park
        self.perception = parent.shared.perception

        # self.trajectory = self.plan.trajectory # to controller
        self.global_path = self.shared.global_path  # from localizer
        
        self.motion = Motion(self.shared, self.plan, self.ego, self.parking)

    def run(self):
        while True:
            try:
                if self.plan.motion_decision == "go":
                    self.motion.go()
                
                elif self.plan.motion_decision == "diagonal_parking":
                    self.motion.diagonal_step1()
                    self.motion.diagonal_step2()
                    self.motion.diagonal_step3()
                    self.motion.diagonal_step4()
                    self.motion.diagonal_step5()
                    self.motion.diagonal_step6()
                    self.motion.diagonal_step7()
                    self.motion.diagonal_step8()
                    self.motion.diagonal_step9()
                    self.motion.diagonal_step10()
                    self.motion.diagonal_step11()
                    self.motion.diagonal_step12()
                    self.motion.diagonal_step13()

                elif self.plan.motion_decision == "parrallel_parking":
                    self.motion.parrallel_step1()
                    self.motion.parrallel_step2()
                    self.motion.parrallel_step3()
                    self.motion.parrallel_step4()
                    self.motion.parrallel_step5()
                    self.motion.parrallel_step6()
                    self.motion.parrallel_step7()
                    self.motion.parrallel_step8()

                elif self.plan.motion_decision == "delivery":
                    self.motion.delivery_step1()
                    self.motion.delivery_step2()
                    self.motion.delivery_step3()
                    self.motion.delivery_step4()
                
                elif self.plan.motion_decision == "obs_tmp":
                    # self.motion.potential_field()

                    # Obs avoidance for morai
                    # mid =[98.1, 116.1]
                    # mid2 =[106.0, 122.4]
                    # ex = self.motion.get_three_points([[mid, 2.3, 5.9], [mid2, 2.3, 5.9]])
                    # middle, start_ind, final_ind = self.motion.find_target_points(ex)
                    # self.motion.make_path(middle, start_ind, final_ind)


                    # Obs avoidance for real world
                    ex = self.motion.get_three_points(self.perception.obs_list)
                    middle, start_ind, final_ind = self.motion.find_target_points(ex)
                    self.motion.make_path(middle, start_ind, final_ind)

                else:
                    pass

            except IndexError:
                print("++++++++motion_planner+++++++++")

                sleep(self.period)