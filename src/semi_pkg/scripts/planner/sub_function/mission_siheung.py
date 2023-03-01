from math import sqrt
from time import time, sleep
from math import cos, sin, pi, sqrt


class Mission():
    def __init__(self, sh, eg, pc, pl):
        self.perception = pc
        self.shared = sh
        self.ego = eg
        self.plan = pl
        self.parking = self.shared.park

        self.time_checker = False
        
        self.obstacle_checker = False
        self.emergency_check = False
        self.obstacle_stop = False

        self.now = 0
        self.parking_create = False
        self.parking_path_maker = False
        self.parking_forward_start = False
        self.parking_backward_start = False
        self.parking_switch = False
        self.force_switch = False
        self.inflection_switch = False
        self.first_stop = False
        self.second_stop = False

        self.turn_left_check = False

        self.speed = 10

    def range(self, a, b = 50):
        return (a-b) <= self.ego.index <= a

    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed

    def go(self):
        self.ego.target_estop = 0x00
        self.ego.target_gear = 0
        self.ego.target_speed = self.speed
        self.plan.behavior_decision = "driving"

        if self.range(1829, 85) and self.turn_left_check == False:
            self.plan.behavior_decision = "stop"
            self.target_control(100, 0)
            sleep(3)
            self.plan.behavior_decision = "driving"
            self.turn_left_check = True
            self.target_control(0, self.speed)

    def Parking_stop_function(self, index1, index2):
        self.plan.behavior_decision = "driving"
        self.target_control(0, 5)
        if ((self.parking_create == False) and (index1 <= self.ego.index <= index2)):
            self.plan.behavior_decision = "stop"
            self.target_control(200, 0)
            sleep(3)
            self.parking.select_num = self.perception.parking_num
            self.target_control(0, 5)
            self.parking_create = True
            self.plan.behavior_decision = "parking_trajectory_Create"

    def Parking_Siheung_diagonal(self):
        if (self.parking_create == False):
            # if (20 <= self.ego.index <= 40) and self.first_stop == False: # Siheung
            if (910 <= self.ego.index <= 930) and self.first_stop == False: # K-City
                self.plan.behavior_decision = "stop"
                self.target_control(75, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.first_stop = True
            if self.first_stop == True and ((self.parking.select_num == 1) or (self.parking.select_num == 2) or (self.parking.select_num == 3)):
                self.target_control(0, 5)
                self.parking_create = True
                self.plan.behavior_decision = "parking_trajectory_Create"
            elif self.first_stop == True and self.parking.select_num == 4 or self.parking.select_num == 5 or self.parking.select_num == 6:
                # self.Parking_stop_function(115, 135) # Siheung
                self.Parking_stop_function(1025, 1045) # K-City

    def Parking_KCity_diagonal(self):
        print(self.parking.select_num)
        if (self.parking_create == False):
            if (735 <= self.ego.index <= 805) and self.first_stop == False: # K-City
                self.plan.behavior_decision = "stop"
                self.target_control(200, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.first_stop = True
            if self.first_stop == True and ((self.parking.select_num == 1) or (self.parking.select_num == 2) or (self.parking.select_num == 3)):
                self.target_control(0, 5)
                self.parking_create = True
                self.plan.behavior_decision = "parking_trajectory_Create"
            elif self.first_stop == True and self.parking.select_num == -1 or self.parking.select_num == 4 or self.parking.select_num == 5 or self.parking.select_num == 6:
                self.Parking_stop_function(865, 915) # K-City

        if (self.parking_create and self.parking_switch == False):
            if (self.parking_forward_start == False and len(self.parking.forward_path.x) > 0):
                self.parking.on = "on"
                self.plan.behavior_decision = "parkingForwardOn"
                self.parking_forward_start = True
            if (15 <= int(self.parking.stop_index - self.parking.index) <= 45) and (self.parking.direction == 0):
                    self.target_control(200, 0)
                    sleep(3)
                    self.plan.behavior_decision = "parkingBackwardOn"
                    self.ego.target_gear = 2
                    self.target_control(0, 5)
            elif (15 <= int(self.parking.stop_index - self.parking.index) <= 25) and (self.parking.direction == 2):
                    self.target_control(100, 0)
                    sleep(3)
                    self.plan.behavior_decision = "driving"
                    self.parking.on = "off"
                    self.ego.target_gear = 0
                    self.target_control(0, self.speed)
                    self.parking_switch = True

    def static_obstacle(self):
        self.plan.behavior_decision = "static_obstacle_avoidance"
        index = len(self.perception.objx)

        # if (2137 < self.ego.index < 2157) and self.obstacle_stop == False:
        #     self.target_control(75, 0)
        #     sleep(3)
        #     self.target_control(0, self.speed)
        #     self.obstacle_stop = True
        
        if (len(self.perception.objx) > 0):
            self.obs_dis = 15.5
            for i in range(0, index):
                self.dis = sqrt(
                    (self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
                self.obs_dis = min(self.obs_dis, self.dis)
                # print(len(self.perception.objx), " ", self.obs_dis)

            if self.obs_dis <= 15:
                self.target_control(0, 5)
                self.obstacle_checker = True
                self.time_checker = False
                
        elif self.obstacle_checker == True:
            if self.time_checker == False:
                self.cur_t = time()
                self.time_checker = True
            if time() - self.cur_t < 5:
                self.target_control(0, 5)
            else:
                self.target_control(0, 7)

        else:
            self.target_control(0, 7)

    def turn_left(self):
        if self.perception.tleft == 1:
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
        else:
            if self.range(229, 85):
                self.plan.behavior_decision = "stop"
                self.target_control(100, 0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

    def emergency_stop(self):
        self.plan.behavior_decision = "emergency_avoidance"
        if self.shared.plan.obstac == True:
            self.target_control(200, 0)
            sleep(3)
            self.target_control(0, 10)

    def convert_lidar(self):
        theta = (self.ego.heading) * pi / 180
        size = 0
        objx = []
        objy = []
        self.perception.tmp_lidar_lock.acquire()
        size = len(self.perception.tmp_objx)
        if(size != 0):
            for i in range(size):
                objx.append(self.perception.tmp_objx[i] * cos(theta) + self.perception.tmp_objy[i] * -sin(theta) + self.ego.x)
                objy.append(self.perception.tmp_objx[i] * sin(theta) + self.perception.tmp_objy[i] * cos(theta) + self.ego.y)
    
        self.perception.lidar_lock.acquire()   
        self.perception.objy = []
        self.perception.objx = []
        self.perception.objx = objx
        self.perception.objy = objy
        self.perception.objw = self.perception.tmp_objw
        self.perception.objh = self.perception.tmp_objh
        self.perception.lidar_lock.release()
        self.perception.tmp_lidar_lock.release()