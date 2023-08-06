#!/usr/bin/env python3
import threading
from time import sleep

class MissionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
    
        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan
               
    def run(self):
        while True:
            try:
                if self.plan.mission_decision == "go":
                    self.plan.behavior_decision = "go"
                    
                elif self.plan.mission_decision == "parrallel_parking":
                    self.plan.behavior_decision = "parrallel_parking"
                    
                elif self.plan.mission_decision == "diagonal_parking":
                    self.plan.behavior_decision = "diagonal_parking"

                elif self.plan.mission_decision == "delivery":
                    self.plan.behavior_decision = "delivery"
                
                elif self.plan.mission_decision == "obs_tmp":
                     self.plan.behavior_decision = "obs_tmp"  

            except IndexError:
                print("++++++++mission_planner+++++++++")

            sleep(self.period)