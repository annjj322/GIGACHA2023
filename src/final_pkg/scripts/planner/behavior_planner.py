#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.mission import Mission
from .sub_function.parking_parallel_lidar import PL

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.mission = Mission(self.shared, self.ego,
                               self.perception, self.plan)
        self.pl = PL(self.ego)

        self.state_remember = "go"

    def run(self):
        while True:
            try:
                self.perception.delivery_lidar_lock.acquire()
                if (self.perception.sign_num != 0):
                    self.mission.convert_delivery()
                self.perception.delivery_lidar_lock.release()

                if self.state_remember != self.plan.state:
                    self.state_remember = self.plan.state
                    self.mission.time_checker = False

                if self.plan.state == "parking":
                    self.mission.go()
                    # self.mission.Parking_KCity_Parallel()
                
                elif self.plan.state == "U-TURN":
                    self.mission.go()

                    # self.mission.u_turn()

                elif self.plan.state == "static_obstacle_detected":
                    # self.mission.convert_lidar()
                    # self.mission.static_obstacle()
                    self.mission.go()

                elif self.plan.state == "left_sign_detected":
                    # self.mission.turn_left()
                    self.mission.go()   

                elif self.plan.state == "non_right_sign":
                    # self.mission.non_traffic_right()
                    self.mission.go()

                elif self.plan.state == "pickup":
                    # self.mission.pickup()
                    self.mission.go()

                elif self.plan.state == "delivery":
                    # self.mission.delivery()
                    self.mission.go()
                    

                elif self.plan.state == "go":
                    self.mission.go()

                else:
                    self.mission.go()

            except IndexError:
                # pass
                print("++++++++behavior_planner+++++++++")

            sleep(self.period)
