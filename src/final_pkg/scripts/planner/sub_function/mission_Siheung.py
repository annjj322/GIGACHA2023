# from math import sqrt
# from time import time, sleep
# from math import cos, sin, pi, sqrt

# class Mission():
#     def __init__(self, sh, eg, pc, pl):
#         self.perception = pc
#         self.shared = sh
#         self.ego = eg
#         self.plan = pl
#         self.parking = self.shared.park

#         self.time_checker = False
#         self.vote_checker = False

#         self.obstacle_checker = False
#         self.encoder_checker = False
#         self.sign_checker = False

#         self.parking_create = False
#         self.parking_backward_start = False
#         self.parking_switch = False
#         self.force_switch = False
#         self.inflection_switch = False
#         self.first_stop = False
#         self.second_stop = False

#         self.selected = 0
#         self.vote = {"345":0, "354":0, "435":0, "453":0, "534":0, "543":0}
#         self.init_dis = 0.0

#         self.signx = 0
#         self.signy = 0
#         self.B_x = [0,0,0]
#         self.B_y = [0,0,0]
#         self.vote_list = [0,0,0]
#         self.target = 0
#         self.pickup_checker = False
#         self.delivery_checker = False
#         self.voting_checker = False

#         self.non_traffic_right_checker = 0
#         self.uturn_stop = False

#         self.speed_check = False
#         self.sp = 0

#         self.speed = 10

#         self.save = 0

#     def range(self, a):
#         return (a-85) <= self.ego.index <= a

#     def target_control(self, brake, speed):
#         self.ego.target_brake = brake
#         self.ego.target_speed = speed

#     def go(self):
#         self.plan.behavior_decision = "driving"
#         # self.target_control(0, 10)
#         # if self.range(600):
#         #     self.target_control(200, 0)
#         # else:
#         #     self.target_control(0, self.speed)

#         # if self.perception.tgreen == 1:
#         #     self.plan.behavior_decision = "driving"
#         #     self.target_control(0, self.speed)
#         # else:
#         #     if self.range(1614) or self.range(2172) or self.range(3533) or self.range(6692) or self.range(6708) or self.range(8026) or self.range(8497):
#         #         # self.plan.behavior_decision = "stop"
#         #         # self.target_control(200,0)
#         #         pass
#         #     else:
#         #         self.plan.behavior_decision = "driving"
#         #         self.target_control(0, self.speed)

#     def Parking_Siheung_Parallel(self):
#         if (self.parking_create == False):
#             if (75 <= self.ego.index <= 105) and self.first_stop == False:
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.parking.select_num = self.perception.parking_num
#                 self.first_stop = True
#                 if self.parking.select_num == 1:
#                     self.target_control(0, 5)
#                     self.parking_create = True
#                     self.plan.behavior_decision = "parking_trajectory_Create"
#                 else:
#                     self.target_control(0, 5)
#             elif self.first_stop == True and (265 <= self.ego.index <= 295) and self.second_stop == False:
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.parking.select_num = self.perception.parking_num
#                 self.second_stop = True
#                 if self.parking.select_num == 2:
#                     self.target_control(0, 5)
#                     self.parking_create = True
#                     self.plan.behavior_decision = "parking_trajectory_Create"
#                 else:
#                     self.target_control(0, 5)
#             elif self.second_stop == True and (465 <= self.ego.index <= 495):
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.parking.select_num = self.perception.parking_num
#                 self.target_control(0, 5)
#                 self.parking_create = True
#                 self.plan.behavior_decision = "parking_trajectory_Create"

#         if (self.parking_create and self.parking_switch == False):
#             if (self.parking_backward_start == False and len(self.parking.forward_path.x) > 0) and (self.parking.mindex + 25 <= self.ego.index <= self.parking.mindex + 45):
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.plan.behavior_decision = "parkingBackwardOn"
#                 self.ego.target_gear = 2
#                 self.target_control(0, 5)
#                 self.parking.on = "on"
#                 self.parking_backward_start = True
#             if (self.parking.direction == 2):
#                 if (1 <= self.parking.index <= 20) and self.force_switch == False:
#                     self.target_control(200, 0)
#                     # sleep(2)
#                     self.target_control(0, 5)
#                     self.force_switch = True
#                     self.parking.on = "forced"
#                     self.ego.target_steer = 27
#                 # elif (1 <= abs(int(self.parking.inflection_point - self.parking.index)) <= 10) and self.inflection_switch == False:
#                 elif (35 <= self.parking.index <= 50) and self.inflection_switch == False:
#                     self.target_control(150, 0)
#                     sleep(2)
#                     self.inflection_switch = True
#                     self.target_control(0, 5)
#                     self.parking.on = "forced"
#                     self.ego.target_steer = -27
#                 elif (10 <= int(self.parking.stop_index - self.parking.index) <= 20):
#                     self.target_control(200, 0)
#                     sleep(3)
#                     self.plan.behavior_decision = "parkingForwardOn"
#                     self.ego.target_gear = 0
#                     self.target_control(0, 5)
#                     self.parking.on = "forced"
#                     self.ego.target_steer = -27
#             # elif (1 <= abs(int(len(self.parking.forward_path.x) - self.parking.inflection_point - self.parking.index)) <= 5) and (self.parking.direction == 0):
#             elif (30 <= self.parking.index <= 55) and (self.parking.direction == 0):
#                     self.target_control(200, 0)
#                     sleep(2)
#                     self.plan.behavior_decision = "driving"
#                     self.target_control(0, 5)
#                     self.parking.on = "off"
#                     self.parking_switch = True

#     def Parking_KCity_Parallel(self):
#         if (self.parking_create == False):
#             if (9515 <= self.ego.index <= 9575) and self.first_stop == False:
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.parking.select_num = self.perception.parking_num
#                 self.first_stop = True
#                 if (self.parking.select_num == 1) or (self.parking.select_num == 2):
#                     self.target_control(0, 5)
#                     self.parking_create = True
#                     self.plan.behavior_decision = "parking_trajectory_Create"
#                 else:
#                     self.target_control(0, 5)
#             elif self.first_stop == True and (9685 <= self.ego.index <= 9745) and self.second_stop == False:
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.parking.select_num = self.perception.parking_num
#                 self.second_stop = True
#                 if self.parking.select_num == 3:
#                     self.target_control(0, 5)
#                     self.parking_create = True
#                     self.plan.behavior_decision = "parking_trajectory_Create"
#                 else:
#                     self.target_control(0, 5)
#             elif self.second_stop == True and (9885 <= self.ego.index <= 9945):
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.parking.select_num = self.perception.parking_num
#                 self.target_control(0, 5)
#                 self.parking_create = True
#                 self.plan.behavior_decision = "parking_trajectory_Create"

#         if (self.parking_create and self.parking_switch == False):
#             if ((self.parking_backward_start == False) and len(self.parking.forward_path.x) > 0) and (self.parking.mindex + 15 <= self.ego.index <= self.parking.mindex + 30):
#                 self.target_control(200, 0)
#                 sleep(3)
#                 self.plan.behavior_decision = "parkingBackwardOn"
#                 self.parking.on = "on"
#                 self.ego.target_gear = 2
#                 self.target_control(0, 5)
#                 self.parking_backward_start = True
#             if (self.parking.direction == 2):
#                 if (1 <= self.parking.index <= 20) and self.force_switch == False:
#                     self.target_control(200, 0)
#                     # sleep(2)
#                     self.target_control(0, 5)
#                     self.force_switch = True
#                     self.parking.on = "forced"
#                     self.ego.target_steer = 27
#                 # elif (1 <= abs(int(self.parking.inflection_point - self.parking.index)) <= 10) and self.inflection_switch == False:
#                 elif (35 <= self.parking.index <= 50) and self.inflection_switch == False:
#                     self.target_control(200, 0)
#                     sleep(2)
#                     self.inflection_switch = True
#                     self.target_control(0, 5)
#                     self.parking.on = "forced"
#                     self.ego.target_steer = -27
#                 elif (7 <= int(self.parking.stop_index - self.parking.index) <= 17):
#                     self.target_control(200, 0)
#                     sleep(3)
#                     self.plan.behavior_decision = "parkingForwardOn"
#                     self.ego.target_gear = 0
#                     self.target_control(0, 5)
#                     self.parking.on = "forced"
#                     self.ego.target_steer = -27
#             # elif (1 <= abs(int(len(self.parking.forward_path.x) - self.parking.inflection_point - self.parking.index)) <= 5) and (self.parking.direction == 0):
#             elif (25 <= self.parking.index <= 40) and (self.parking.direction == 0):
#                     self.parking.on = "off"
#                     self.plan.behavior_decision = "driving"
#                     self.target_control(0, self.speed)
#                     self.parking_switch = True

#     def u_turn(self):
#         self.perception.tleft = 1
#         if self.perception.tleft == 1 :
#             self.plan.behavior_decision = "driving"
#             if (5175 < self.ego.index < 5335):
#                 self.parking.on = "U_turn"
#             if self.range(5345) and self.uturn_stop == False:
#                     # self.plan.behavior_decision = "stop"
#                     # self.target_control(75, 0)
#                     # sleep(3)
#                     self.plan.behavior_decision = "driving"
#                     self.parking.on = "forced"
#                     self.target_control(0, 5)
#                     self.ego.target_steer = -27
#                     self.uturn_stop = True
#             elif self.ego.index > 5407 and self.uturn_stop == True:
#                 self.parking.on = "off"
#         else:
#             if self.range(5375):
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#             else:
#                 self.plan.behavior_decision = "driving"
#                 self.target_control(0, self.speed)

#     def static_obstacle(self):
#         self.plan.behavior_decision = "static_obstacle_avoidance"
#         index = len(self.perception.objx)

#         if (len(self.perception.objx) > 0):
#             self.obs_dis = 15.5
#             for i in range(0, index):
#                 self.dis = sqrt(
#                     (self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
#                 self.obs_dis = min(self.obs_dis, self.dis)
#                 print(len(self.perception.objx), " ", self.obs_dis)

#             if self.obs_dis <= 15:
#                 self.target_control(0,7)
#                 self.obstacle_checker = True
#                 self.time_checker = False

#         elif self.obstacle_checker == True:
#             if self.time_checker == False:
#                 self.cur_t = time()
#                 self.time_checker = True
#             if time() - self.cur_t < 5:
#                 self.target_control(0,7)
#             else:
#                 self.target_control(0,self.speed)

#     def turn_right(self):
#         if self.perception.tgreen == 1:
#             self.plan.behavior_decision = "driving"
#             self.target_control(0, self.speed)
#         else:
#             # if self.ego.index >= 410 and self.ego.index <= 470:
#             if self.ego.index >= 600 and self.ego.index <= 650: # Siheung
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#             else:
#                 self.plan.behavior_decision = "driving"
#                 self.target_control(0, self.speed)

#     def turn_left(self):
#         if self.perception.tleft == 1 :
#             self.plan.behavior_decision = "driving"
#             self.target_control(0, 12)
#         else:
#             if self.range(1240):
#                 self.plan.behavior_decision = "stop"
#                 self.target_control(75, 0)
#             else:
#                 self.plan.behavior_decision = "driving"
#                 self.target_control(0, 12)
#         # if self.perception.tleft == 1 :
#         #     self.plan.behavior_decision = "driving"
#         #     self.target_control(0, self.speed)
#         # else:
#         #     if self.range(1237):
#         #         self.plan.behavior_decision = "stop"
#         #         self.target_control(200, 0)
#         #     else:
#         #         self.plan.behavior_decision = "driving"
#         #         self.target_control(0, self.speed)

#     def non_traffic_right(self):
#         # if (self.range(2032, 20) and self.non_traffic_right_checker == 0) or (self.range(2146, 20) and self.non_traffic_right_checker == 1):
#         #     self.plan.behavior_decision = "stop"
#         #     self.target_control(200, 0)
#         #     sleep(3)
#         #     self.plan.behavior_decision = "driving"
#         #     self.target_control(0, self.speed)
#         #     self.non_traffic_right_checker += 1
#         pass

#     def convert_lidar(self):
#         theta = (self.ego.heading) * pi / 180
#         size = 0
#         objx = []
#         objy = []
#         self.perception.tmp_lidar_lock.acquire()
#         size = len(self.perception.tmp_objx)
#         if(size != 0):
#             for i in range(size):
#                 objx.append(self.perception.tmp_objx[i] * cos(theta) + self.perception.tmp_objy[i] * -sin(theta) + self.ego.x)
#                 objy.append(self.perception.tmp_objx[i] * sin(theta) + self.perception.tmp_objy[i] * cos(theta) + self.ego.y)

#         self.perception.lidar_lock.acquire()
#         self.perception.objy = []
#         self.perception.objx = []
#         self.perception.objx = objx
#         self.perception.objy = objy
#         self.perception.objw = self.perception.tmp_objw
#         self.perception.objh = self.perception.tmp_objh
#         self.perception.lidar_lock.release()
#         self.perception.tmp_lidar_lock.release()

#     def convert_delivery(self):
#         theta = (self.ego.heading) * pi / 180
#         size = 0

#         if(self.perception.signx != 0):
#             self.signx = self.perception.signx * cos(theta) + self.perception.signy * -sin(theta) + self.ego.x
#             self.signy = self.perception.signx * sin(theta) + self.perception.signy * cos(theta) + self.ego.y

#         #self.perception.delivery_lidar_lock.acquire()
#         for i in range(3):
#             if(self.perception.B_x[i] != 0):
#                 self.B_x[i] = self.perception.B_x[i] * cos(theta) + self.perception.B_y[i] * -sin(theta) + self.ego.x
#                 self.B_y[i] = self.perception.B_x[i] * sin(theta) + self.perception.B_y[i] * cos(theta) + self.ego.y
#         #self.perception.delivery_lidar_lock.release()


#     def pickup(self):
#         if self.pickup_checker == False:
#             self.plan.behavior_decision = "pickup_mode"

#         if self.perception.signx != 0 and self.vote_checker == False:
#             self.vote_checker = True
#             count = 0
#             while count != 45:
#                 print("Vote list : ", self.vote_list)
#                 self.vote_list[self.perception.target-1] += 1
#                 count +=1
#             self.target = self.vote_list.index(max(self.vote_list)) + 1
#         # print("target : ", self.target)

#         sign_dis = 0.0
#         sign_dis = self.perception.signx

#         if 0 < sign_dis < 8 and self.pickup_checker == False:
#             if not self.encoder_checker:
#                 print('#######sign distance : ', sign_dis)
#                 self.encoder_checker = True
#                 self.init_dis = self.ego.dis
#                 self.save = self.perception.signx
#                 self.sign_checker = True
#         elif 0 < sign_dis < 10 and self.pickup_checker == False:
#             self.target_control(0, 5)
#             self.plan.behavior_decision = "pickup"

#         if self.sign_checker and self.pickup_checker == False:
#             print("encoder checking : ", self.ego.dis - self.init_dis)
#             if self.ego.dis - self.init_dis > 7:
#             # if self.ego.dis - self.init_dis > self.save - 1:
#                 self.pickup_checker = True
#                 # self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(6)
#                 self.target_control(0, self.speed)
#                 self.plan.behavior_decision = "pickup_end"
#                 self.encoder_checker = False
#                 self.sign_checker = False


#     def delivery(self):
#         # self.target_control(0, 7)
#         self.plan.behavior_decision = "delivery_mode"
#         sign_dis = 0.0
#         if(self.perception.B_x[self.target - 1]!=0):
#             sign_dis = self.perception.B_x[self.target - 1]
#         # print('#######sign distance : ', sign_dis)
#         # print(self.perception.B_x)

#         if (0 < sign_dis < 8 and self.delivery_checker == False):
#             if not self.encoder_checker:
#                 self.encoder_checker = True
#                 self.init_dis = self.ego.dis
#                 self.sign_checker = True
#         elif 0 < sign_dis < 10 and self.delivery_checker == False:
#             self.target_control(0, 5)
#             self.plan.behavior_decision = "delivery"

#         if self.sign_checker and self.delivery_checker == False:
#             print("encoder checking : ", self.ego.dis - self.init_dis)
#             if self.ego.dis - self.init_dis > 7:
#                 self.delivery_checker = True
#                 # self.plan.behavior_decision = "stop"
#                 self.target_control(200, 0)
#                 sleep(6)
#                 self.target_control(0, self.speed)
#                 self.plan.behavior_decision = "delivery_end"


#     # def pickup(self):
#     #     self.plan.behavior_decision = "delivery_mode"
#     #     sign_dis = 0.0
#     #     sign_dis = sqrt((self.perception.signx - self.ego.x)**2 + (self.perception.signy - self.ego.y)**2)
#     #     # print("pickup : " , sign_dis)
#     #     if 0 < sign_dis < 1.3 and self.pickup_checker == False:
#     #         self.pickup_checker = True
#     #         self.plan.behavior_decision = "stop"
#     #         self.target_control(200, 0)
#     #         sleep(5)
#     #         self.target_control(0, self.speed)
#     #         self.plan.behavior_decision = "pickup_end"
#     #         self.voting()
#     #     elif 0 < sign_dis < 10:
#     #         self.plan.behavior_decision = "pickup"
#     #     if (self.pickup_checker == True):
#     #         self.delivery()

#     # def delivery(self):
#     #     self.plan.behavior_decision = "delivery"
#     #     sign_dis = sqrt((self.perception.B_x[self.selected] - self.ego.x)**2 + (self.perception.B_y[self.selected] - self.ego.y)**2)
#     #     print("delivery : ", sign_dis)
#     #     if(0 < sign_dis < 1.2 and self.delivery_checker == False):
#     #         self.delivery_checker = True
#     #         self.plan.behavior_decision = "stop"
#     #         self.target_control(200, 0)
#     #         sleep(5)
#     #         self.target_control(0, self.speed)
#     #     self.plan.behavior_decision = "delivery_end"