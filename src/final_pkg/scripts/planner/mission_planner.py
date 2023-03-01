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
                if self.shared.perception.signname == "static_obstacle":
                    self.plan.state = "static_obstacle_detected"           

                elif self.shared.perception.signname == "delivery":
                    self.plan.state = "delivery"

                elif self.shared.perception.signname == "pickup":
                    self.plan.state = "pickup"

                elif self.shared.perception.signname == "turn_left_traffic_light":
                    self.plan.state = "left_sign_detected"

                elif self.shared.perception.signname == "non_traffic_right":
                    self.plan.state ="non_right_sign"
                
                elif self.perception.signname == "parking":
                    self.plan.state = "parking"

                elif self.perception.signname == "U-TURN":
                    self.plan.state = "U-TURN"

                else:
                    self.plan.state = "go"

            except IndexError:
                print("++++++++mission_planner+++++++++")

            sleep(self.period)