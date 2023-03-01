#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.mission import Mission
from .sub_function.parking_diagonal_lidar import PL

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.mission = Mission(self.shared, self.ego, self.perception, self.plan)

        self.pl = PL(self.ego)
        
        self.state_remember = "go"

    def run(self):
        while True:
            try:
                self.mission.convert_lidar()

                if self.state_remember != self.plan.state:
                    self.state_remember = self.plan.state
                    self.mission.time_checker = False

                if self.plan.state == "parking":
                    ### HANAMJA JUCHA ###
                    # self.mission.Parking_KCity_diagonal()
                    #####################
                    self.mission.Parking_KCity_diagonal_jeongseok()

                elif self.plan.state == "static_obstacle_detected":
                    self.mission.static_obstacle()

                elif self.plan.state == "left_sign_detected":
                    self.mission.turn_left()

                elif self.plan.state == "emergency_stop":
                    self.mission.emergency_stop()
        
            except IndexError:
                print("++++++++behavior_planner+++++++++")

            sleep(self.period)
