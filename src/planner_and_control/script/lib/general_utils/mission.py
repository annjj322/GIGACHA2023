import rospy
from math import sqrt
from time import time

class Mission():
    def __init__(self, eg, pc):
        self.perception = pc
        self.ego = eg
        self.mission_complete = False
        self.behavior_decision = " "
        self.timer = time()
        self.time_checker = False
        self.obstacle_checker = False

    def go(self):
        self.ego.gear = 0
        self.ego.target_speed = 5.0
        self.behavior_decision = "driving"
        
    def parking(self):
        pass   

        
    def stop(self):
        self.sign_dis = sqrt((self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
        if self.sign_dis <= 5:
            if self.go_side_check == False:
                self.behavior_decision = "stop"
                self.wait_time = time()
                self.go_side_check = True
            if self.behavior_decision == "stop" and time() - self.wait_time > 3:
                self.behavior_decision = "go"
                self.sign_detected = 1
        elif self.sign_dis > 5 and self.sign_detected == 0:
            self.behavior_decision = "go_side"
            self.go_side_check = False

    def static_obstacle(self, objx, objy, ego):
        self.ego = ego
        self.behavior_decision = "static_obstacle_avoidance"
        if (len(objx) > 0):
            self.obs_dis = sqrt((objx[0] - self.ego.x)**2 + (objy[0] - self.ego.y)**2)
            if self.obs_dis <= 5:
                self.ego.target_speed = 5.0
                self.obstacle_checker = True
                self.time_checker = False
            elif self.obs_dis > 5 and self.obstacle_checker == True:
                if self.time_checker == False:
                    self.cur_t = time()
                    self.time_checker = True

                if time() - self.cur_t < 3:
                    self.ego.target_speed = 5.0
                else:
                    self.ego.target_speed = 15.0
            else:
                self.ego.target_speed = 15.0

    def turn_right(self):
        if self.perception.tgreen == 1:
            self.behavior_decision = "turn_right"
        else:
            if self.ego.index >= 1000 and self.ego.index <= 1050:
                self.behavior_decision = "stop"
            else:
                self.behavior_decision = "turn_right"

    def non_traffic_right(self):
        if(len(self.perception.rightx)!=0):
            self.right_dis=sqrt((self.perception.rightx[0] - self.ego.x)**2 + (self.perception.righty[0] - self.ego.y)**2)
            if self.right_dis<=5:
                self.behavior_decision = "stop"
                time.sleep(2)
                self.behavior_decision = "turn_right"
    
    def turn_left(self):
        if self.perception.tleft == 1:
            self.behavior_decision = "turn_left"
        else:
            if self.ego.index >= 2750 and self.ego.index <= 2800:
                self.behavior_decision = "stop"
            else:
                self.behavior_decision = "turn_left"

    def child_area(self, signx, signy):
        if (len(self.perception.signx)!= 0):
            self.sign_dis = sqrt((self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
            if self.sign_dis <= 15:
                self.ego.target_speed = 7.0
            else:
                self.ego.target_speed = 20.0
            self.behavior_decision = "child_area"