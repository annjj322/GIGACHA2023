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
        self.vote_checker = False

        self.obstacle_checker = False
        self.encoder_checker = False
        self.sign_checker = False

        self.parking_create = False
        self.parking_backward_start = False
        self.parking_switch = False
        self.force_switch = False
        self.inflection_switch = False
        self.first_stop = False
        self.second_stop = False

        self.sign_count = [0,0]


        self.selected = 0
        self.vote = {"345":0, "354":0, "435":0, "453":0, "534":0, "543":0}
        self.init_dis = 0.0
        self.save = 0

        self.signx = 0
        self.signy = 0
        self.B_x = [0,0,0]
        self.B_y = [0,0,0]

        self.vote_list = [0,0,0]
        self.target = 0
        self.pickup_checker = False
        self.delivery_checker = False
        self.voting_checker = False

        self.non_traffic_right_checker = 0
        self.uturn_stop = False
        self.uturn_checker = False
        self.uturn_checker2 = False
        self.tmp_tleft = 0

        self.speed_check = False
        self.sp = 0

        self.speed = 10


    def range(self, a, b = 50):
        return (a-b) <= self.ego.index <= a

    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed

    def go(self):
        if self.perception.tgreen == 1:
            self.plan.behavior_decision = "driving"
            self.target_control(0, 20)
        else:
            if self.range(1614, 85) or self.range(2172, 85) or self.range(3533, 85) or self.range(6708, 85) or self.range(8026, 85) or self.range(8497, 85):
                # self.plan.behavior_decision = "stop"
                self.plan.behavior_decision = "driving"
                self.target_control(100,0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

    def Parking_KCity_Parallel(self):
        if (self.parking_create == False):
            if (9515 <= self.ego.index <= 9565) and self.first_stop == False:
                # self.plan.behavior_decision = "stop"
                self.plan.behavior_decision = "driving"
                self.target_control(100, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.first_stop = True
                if (self.parking.select_num == 1) or (self.parking.select_num == 2):
                    self.target_control(0, 5)
                    self.parking_create = True
                    # self.plan.behavior_decision = "parking_trajectory_Create"
                    self.plan.behavior_decision = "driving"
                else:
                    self.target_control(0, 5)
            elif self.first_stop == True and (9600 <= self.ego.index <= 9650):
                # self.plan.behavior_decision = "stop"
                self.plan.behavior_decision = "driving"
                self.target_control(100, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                if (self.parking.select_num == 2) or (self.parking.select_num == 3):
                    self.target_control(0, 5)
                    self.parking_create = True
                    # self.plan.behavior_decision = "parking_trajectory_Create"
                    self.plan.behavior_decision = "driving"
                else:
                    self.target_control(0, 10)

        if (self.parking_create and self.parking_switch == False):
            if ((self.parking_backward_start == False) and len(self.parking.forward_path.x) > 0) and (self.parking.mindex + 15 <= self.ego.index <= self.parking.mindex + 30):
                self.target_control(100, 0)
                sleep(3)
                # self.plan.behavior_decision = "parkingBackwardOn"
                self.plan.behavior_decision = "driving"
                self.parking.on = "on"
                self.ego.target_gear = 2
                self.target_control(0, 5)
                self.parking_backward_start = True
            if (self.parking.direction == 2):
                if (1 <= self.parking.index <= 20) and self.force_switch == False:
                    self.target_control(0, 5)
                    self.force_switch = True
                    self.parking.on = "forced"
                    self.ego.target_steer = 27
                # elif (1 <= abs(int(self.parking.inflection_point - self.parking.index)) <= 10) and self.inflection_switch == False:
                elif (35 <= self.parking.index <= 50) and self.inflection_switch == False:
                    self.target_control(100, 0)
                    sleep(2)
                    self.inflection_switch = True
                    self.target_control(0, 5)
                    self.parking.on = "forced"
                    self.ego.target_steer = -27
                elif (7 <= int(self.parking.stop_index - self.parking.index) <= 17):
                    self.target_control(100, 0)
                    self.parking.on = "forced"
                    self.ego.target_steer = 0
                    sleep(11)
                    # self.plan.behavior_decision = "parkingForwardOn"
                    self.plan.behavior_decision = "driving"
                    self.parking.on = "forced"
                    self.ego.target_steer = -27
                    self.ego.target_gear = 0
                    self.target_control(0, 5)
            
            elif (27 <= self.parking.index <= 40) and (self.parking.direction == 0):
                    self.parking.on = "off"
                    self.plan.behavior_decision = "driving"
                    self.target_control(0, self.speed)
                    self.parking_switch = True

    def u_turn(self):
        if self.perception.tleft == 1 or 35 <= abs(time() - self.sign_count[0]) <= 43 or self.uturn_checker:
            if self.range(5375, 50):
                self.uturn_checker = True

            if (5175 < self.ego.index < 5325) and self.uturn_checker2 == False:
                self.parking.on = "U_turn"
            if self.range(5375) and self.uturn_stop == False:
                self.uturn_checker2 = True
                # self.plan.behavior_decision = "U_turn"
                self.plan.behavior_decision = "driving"
                self.parking.on = "forced"
                self.target_control(0, 5)
                self.ego.target_steer = -27
                self.uturn_stop = True
            elif self.ego.index > 5407 and self.uturn_stop == True:
                self.plan.behavior_decision = "driving"
                self.parking.on = "off"
                self.uturn_checker = False
        else:
            if self.range(5375, 50):
                # self.plan.behavior_decision = "stop"
                self.plan.behavior_decision = "driving"
                self.target_control(100, 0)
                print('34 time : ', abs(time() - self.sign_count[0]))
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

    def static_obstacle(self):
        # self.plan.behavior_decision = "static_obstacle_avoidance"
        self.plan.behavior_decision = "driving"
        index = len(self.perception.objx)

        if (len(self.perception.objx) > 0):
            self.obs_dis = 15.5
            for i in range(0, index):
                self.dis = sqrt(
                    (self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
                self.obs_dis = min(self.obs_dis, self.dis)
                # print(len(self.perception.objx), " ", self.obs_dis)

            if self.obs_dis <= 10:
                self.target_control(0, 7)
                self.obstacle_checker = True
                self.time_checker = False

        elif self.obstacle_checker == True:
            if self.time_checker == False:
                self.cur_t = time()
                self.time_checker = True
            if time() - self.cur_t < 5:
                self.target_control(0, 7)
            else:
                self.target_control(0, self.speed)

    def turn_left(self):
        if self.perception.tleft:
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
            if self.sign_count[0] == 0 and self.sign_count[1] != 0:
                self.sign_count[0] = time()
                self.sign_count[1] = 0
        else:
            if self.range(4609, 50):
                # self.plan.behavior_decision = "stop"
                self.plan.behavior_decision = "driving"
                self.target_control(100, 0)
                self.sign_count[1] = 1
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

    def non_traffic_right(self):
        if (self.range(5597, 50) and self.non_traffic_right_checker == 0) or (self.range(5821, 50) and self.non_traffic_right_checker == 1):
            # self.plan.behavior_decision = "stop"
            self.plan.behavior_decision = "driving"
            self.target_control(100, 0)
            sleep(3)
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
            self.non_traffic_right_checker += 1

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

    def convert_delivery(self):
        theta = (self.ego.heading) * pi / 180
        size = 0

        if(self.perception.signx != 0):
            self.signx = self.perception.signx * cos(theta) + self.perception.signy * -sin(theta) + self.ego.x
            self.signy = self.perception.signx * sin(theta) + self.perception.signy * cos(theta) + self.ego.y

        #self.perception.delivery_lidar_lock.acquire()
        for i in range(3):
            if(self.perception.B_x[i] != 0):
                self.B_x[i] = self.perception.B_x[i] * cos(theta) + self.perception.B_y[i] * -sin(theta) + self.ego.x
                self.B_y[i] = self.perception.B_x[i] * sin(theta) + self.perception.B_y[i] * cos(theta) + self.ego.y
        #self.perception.delivery_lidar_lock.release()

    def pickup(self):
        if self.pickup_checker == False:
            # self.plan.behavior_decision = "pickup_mode"
            self.plan.behavior_decision = "driving"

        if self.perception.signx != 0 and self.vote_checker == False:
            self.vote_checker = True
            count = 0
            while count != 45:
                print("Vote list : ", self.vote_list)
                self.vote_list[self.perception.target-1] += 1
                count +=1
            self.target = self.vote_list.index(max(self.vote_list)) + 1
        # print("target : ", self.target)

        sign_dis = 0.0
        sign_dis = self.perception.signx

        if 0 < sign_dis < 8 and self.pickup_checker == False:
            if not self.encoder_checker:
                self.encoder_checker = True
                self.init_dis = self.ego.dis
                self.save = self.perception.signx
                print('#######sign distance : ', self.save)
                self.sign_checker = True
        elif 0 < sign_dis < 10 and self.pickup_checker == False:
            self.target_control(0, 5)
            # self.plan.behavior_decision = "pickup"
            self.plan.behavior_decision = "driving"

        if self.sign_checker and self.pickup_checker == False:
            print("encoder checking : ", self.ego.dis - self.init_dis)
            # if self.ego.dis - self.init_dis > 7:
            if self.ego.dis - self.init_dis > self.save - 1.0:
                self.pickup_checker = True
                # self.plan.behavior_decision = "stop"
                self.target_control(200, 0)
                sleep(6)
                self.target_control(0, 10)
                # self.plan.behavior_decision = "pickup_end"
                self.plan.behavior_decision = "driving"
                self.encoder_checker = False
                self.sign_checker = False


    def delivery(self):
        if self.delivery_checker == False:
            # self.plan.behavior_decision = "delivery_mode"
            self.plan.behavior_decision = "driving"

        sign_dis = 0.0
        if(self.perception.B_x[self.target - 1]!=0):
            sign_dis = self.perception.B_x[self.target - 1]
        # print('#######sign distance : ', sign_dis)
        # print(self.perception.B_x)

        if (0 < sign_dis < 8 and self.delivery_checker == False):
            if not self.encoder_checker:
                self.encoder_checker = True
                self.init_dis = self.ego.dis
                self.save = self.perception.B_x[self.target - 1]
                print('#######sign distance : ', self.save)
                self.sign_checker = True
        elif 0 < sign_dis < 10 and self.delivery_checker == False:
            self.target_control(0, 5)
            # self.plan.behavior_decision = "delivery"
            self.plan.behavior_decision = "driving"

        if self.sign_checker and self.delivery_checker == False:
            print("encoder checking : ", self.ego.dis - self.init_dis)  
            # if self.ego.dis - self.init_dis > 7:
            if self.ego.dis - self.init_dis > self.save - 1.0:
                self.delivery_checker = True
                # self.plan.behavior_decision = "stop"
                self.target_control(200, 0)
                sleep(6)
                self.target_control(0, 10)
                # self.plan.behavior_decision = "delivery_end"
                self.plan.behavior_decision = "driving"