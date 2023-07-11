#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.mission import Mission
class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.mission = Mission(self.shared, self.ego, self.perception, self.plan)
        
    def run(self):
        while True:
            try:
                if self.plan.state == "go":
                    self.mission.go()

                elif self.plan.state == "parking":
                    
                    # self.mission.Parking_KCity_diagonal_LJY()
                    # self.mission.Parking_KCity_parallel_hy()
                    self.mission.parking_parallel_jm()
                
                elif self.plan.state == "static_obstacle_detected":
                    self.mission.static_obstacle()

                elif self.plan.state == "left_sign_detected":
                    self.mission.turn_left()

                elif self.plan.state == "emergency_stop":
                    self.mission.emergency_stop()
        
            except IndexError:
                print("++++++++behavior_planner+++++++++")

            sleep(self.period)
