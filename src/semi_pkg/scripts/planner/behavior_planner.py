#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.behavior import Behavior

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.behavior = Behavior(self.shared, self.ego, self.perception, self.plan)
        
    def run(self):
        while True:
            try:
                if self.plan.behavior_decision == "go":
                    self.behavior.go()

                elif self.plan.behavior_decision == "parrallel_parking":
                    self.behavior.parrallel_parking()

                elif self.plan.behavior_decision == "diagonal_parking":
                    self.behavior.diagonal_parking()

                elif self.plan.behavior_decision == "delivery":
                    self.behavior.delivery()

                elif self.plan.behavior_decision == "obs_tmp":
                    self.behavior.obs()


        
            except IndexError:
                print("++++++++behavior_planner+++++++++")

            sleep(self.period)
