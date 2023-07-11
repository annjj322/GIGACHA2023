from math import sqrt, hypot
from time import time, sleep
from math import cos, sin, pi, sqrt
from local_pkg.msg import Control_Info
import rospy
import numpy as np


# from . parking_diagonal_LJY_MTR import *

class Mission():
    def __init__(self, sh, eg, pc, pl):

        self.perception = pc
        self.shared = sh
        self.ego = eg
        self.plan = pl
        self.parking = self.shared.park

        self.global_path = self.shared.global_path
        self.time_checker = False
        
        self.obstacle_checker = False
        self.emergency_check = False
        self.obstacle_stop = False

        self.parking_path_maker = False
        self.parking_forward_start = False
        self.parking_backward_start = False
        self.parking_switch = False
        self.parking_create = False
        self.force_switch = False
        self.inflection_switch = False
        
        self.first_stop = False
        self.second_stop = False
        self.third_stop = False
        self.fourth_stop = False
        self.fifth_stop = False
        self.sixth_stop = False
        self.seventh_stop = False
        self.eighth_stop = False

        self.backward_tra_create = False
        self.backward_tra_create1 = False
        self.backward_tra_create2 = False
        self.forward_tra_create = False
        self.forward_reverse_tra_create = False
        self.parallel_flag=False
        self.exit_flag=False
        self.hy_test=False
        self.parking_turning=False
        self.global_path_storage_full = False
        self.global_path_storage_x = []
        self.global_path_storage_y = []


        self.detection = False
    def range(self, a, b):
        return (a-b) <= self.ego.index <= a

    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed

    def go(self):
        self.ego.target_estop = 0x00
        self.ego.target_gear = 0
        self.plan.behavior_decision = "go"

######################################################################################################################################
    def Parking_KCity_diagonal_LJY(self):
        self.shared.flag = True
        if (self.parking_create == False):
            if (len(self.shared.perception.edge_L) != 0) and (self.first_stop == False): # real perception
            # if (len(self.shared.perception.edge_L) == 5) and (self.first_stop == False): # 중간에 멈추는 걸 원치 않을 때
            # if  770 < self.ego.index < 790 : # inha songdo _ using index
            # if  630 < self.ego.index < 650 and self.first_stop ==False:
                if self.global_path_storage_full == False:
                    self.global_path_storage_x = self.global_path.x
                    self.global_path_storage_y = self.global_path.y
                    self.global_path_storage_full = True
                elif self.global_path_storage_full == True:
                    self.target_control(50, 0)
                    print("STOP!!!!!!!!!!!!!!!!!!!!!!!")
                    sleep(3) #3
                    self.first_stop = True
                    

            if (self.first_stop == True) and (self.second_stop == False):
                if self.backward_tra_create == False:
                    self.plan.behavior_decision = "backward_trajectory_Create"
                    self.backward_tra_create = True
                    self.shared.perception.flag = False
                    

                elif self.backward_tra_create == True:
                    self.plan.behavior_decision = "parkingBackwardOn"
                    
                    self.ego.target_gear = 2
                    self.parking.on = "back"
                    
                    self.target_control(0,7)
                    
                    # experiment by jm
                    if self.ego.index<=5:
                        self.target_control(0, 12)
                    

                    if self.ego.index >= len(self.global_path.x)-50:
                        self.target_control(50, 0)
                        print("STOP!!!!!!!!!!!!!!!!!!!!!!!")
                        sleep(3) 
                        self.second_stop = True # 경로와 직선 사이 교점 근처에 정차
                        self.global_path.x = self.global_path_storage_x # 다시 원래 경로로 바꾸어주어야 함
                        self.global_path.y = self.global_path_storage_y

            if (self.second_stop == True) and (self.third_stop == False):
                if self.forward_tra_create == False:
                    self.plan.behavior_decision = "forward_trajectory_Create"
                    print("trajectory is created")
                    sleep(3)
                    self.forward_tra_create = True
                    
                elif self.forward_tra_create == True:
                    self.plan.behavior_decision = "parkingForwardOn"
                    self.ego.target_gear = 0
                    self.parking.on = "forward_tmp"
                    self.target_control(0, 6)
                    if self.ego.index<=5:
                        self.target_control(0, 10)
                    # print("Ldata: ", self.shared.perception.edge_L)
                    # print("Rdata: ", self.shared.perception.edge_R)
                    if self.ego.index >= len(self.global_path.x)-50:
                        self.target_control(50, 0)
                        print("STOP!!!!!!!!!!!!!!!!!!!!!!!")
                        print("diagonal parking complete")
                        sleep(3)
                        self.third_stop = True # 사선 주차 성공

            if (self.third_stop == True) and (self.fourth_stop == False):
                if self.forward_reverse_tra_create == False:
                    self.plan.behavior_decision = "forward_reverse_trajectory_Create"
                    self.forward_reverse_tra_create = True
                elif self.forward_reverse_tra_create == True:
                    self.plan.behavior_decision = "parkingBackwardOn"
                    self.ego.target_gear = 2
                    self.parking.on = "back"
                    self.target_control(0, 5)
                    print("len: ", len(self.global_path.x))
                    print("ego_ind: ", self.ego.index)
                    if self.ego.index >= len(self.global_path.x)-20:
                        self.target_control(60, 0)
                        sleep(3) 
                        self.fourth_stop = True # 경로와 직선 사이 교점 근처에 정차
                        self.parking_create = True # 주차미션 종료
            else: # 주차미션을 부여받지 않은 처음 상태 주행
                # self.go()
                self.plan.state = "go"
                # self.shared.plan.behavior_decision = "go" 
        else: # 원래대로 주행
            self.global_path.x = self.global_path_storage_x # 다시 원래 경로
            self.global_path.y = self.global_path_storage_y
            self.parking.on = "off"
            self.shared.plan.behavior_decision == "go"
            self.plan.state = "go"
            self.ego.target_gear = 0
            # self.target_control(100,0)
            self.shared.flag = False
            # if self.ego.index<=5:
            #     self.target_control(0, 10)
            self.target_control(0,7)
                    

#######################################################################################################################################
    def Parking_KCity_parallel_hy_origin(self):
        # self.shared.plan.behavior_decision = "parking"
        if (self.parking_create == False):
            if (3602 <= self.ego.index <= 3654) and self.first_stop == False: # K-City 
            ##멈추는 송도 기준 정립 필요함!!
            # if (669 <= self.ego.index <=679 ) and self.first_stop == False: # songdo
            # if (720 <= self.ego.index <=730 ) and self.first_stop == False: # songdo
                if self.global_path_storage_full == False:
                    self.global_path_storage_x = self.global_path.x
                    self.global_path_storage_y = self.global_path.y
                    self.global_path_storage_full = True
                    print("global path 저장완료")
                elif self.global_path_storage_full == True:
                    # self.plan.behavior_decision = "stop"
                        #일단 주차 구간에 들어왔으니 멈출게?
                    self.target_control(200, 0)
                    if self.ego.speed<0.5:
                        self.first_stop = True
                        print('ready for parallel parking ')
            elif (self.first_stop == True) and (self.second_stop == False):
                if self.forward_tra_create == False:
                    self.plan.behavior_decision = "forward_trajectory_Create_para"
                    self.forward_tra_create = True #전진 경로 만들었다. 
                elif self.forward_tra_create == True: #전진 경로 만들었으니까 이제 할게?
                    # self.plan.behavior_decision = "parkingForwardOn"
                    self.plan.behavior_decision = "parking"
                    self.ego.target_gear = 0
                     ##'forward'
                    if len(self.global_path.x) - 5 <= self.ego.index:
                        self.target_control( 200,0) #브레이크 값 실험적 구해야 해요
                        if self.ego.speed<0.5:    
                            print('전진 종료')
                            self.second_stop = True
                    else:
                        if self.ego.index<=5:
                            self.target_control(0, 12)
                        else:
                            self.target_control(0, 10)
            elif (self.second_stop == True) and (self.third_stop == False):
                if self.backward_tra_create1 == False:
                    self.plan.behavior_decision = "backward_trajectory_Create_para"
                    self.backward_tra_create1 = True
                    print('경로 생성 완료!!!')
                elif self.backward_tra_create1 == True:
                    self.plan.behavior_decision = "parkingBackwardOn"
                    self.ego.target_gear = 2
                    if self.ego.index<=5:
                        self.target_control(0, 10)
                    else:
                        self.target_control(0, 5)
                    if len(self.global_path.x) - 5 <= self.ego.index :
                        self.target_control(200,0)
                        if self.ego.speed<0.02:
                            self.third_stop= True
                            self.parking.on='off'
                            sleep(2)
            elif (self.third_stop ==True) and (self.fourth_stop ==False) :
                    if self.backward_tra_create2==False:    
                        self.plan.behavior_decision="exit"
                        self.backward_tra_create2=True
                    elif self.backward_tra_create2:
                        self.plan.behavior_decision = "parkingFowardOn"
                        self.ego.target_gear = 0
                        self.target_control(0, 5)
                        if self.ego.index >= len(self.global_path.x)-20:                           
                            self.target_control(20,0)
                            self.parking_create=True
                            self.fourth_stop=True
            else:
               pass
            
        else: # 원래대로 주행
            self.trans_global_path(self.global_path_storage_x,self.global_path_storage_y)
            self.shared.plan.behavior_decision == "go"
            self.plan.state = "go"
            self.target_control(0,10)
                
    #######################################################################################################################################
    def trans_global_path(self,x,y):
        self.global_path.x=x
        self.global_path.y=y
        self.global_path.mission = []
        for i in range(len(self.global_path.x)):
            self.global_path.mission.append("go")
    
    def Parking_KCity_parallel_hy(self):
        # self.shared.plan.behavior_decision = "parking"
        if (self.parking_create == False):
            if (3602 <= self.ego.index <= 3654) and self.first_stop == False: # K-City 
            ##멈추는 송도 기준 정립 필요함!!
            # if (669 <= self.ego.index <=679 ) and self.first_stop == False: # songdo
            # if (720 <= self.ego.index <=730 ) and self.first_stop == False: # songdo
                if self.global_path_storage_full == False:
                    self.global_path_storage_x = self.global_path.x
                    self.global_path_storage_y = self.global_path.y
                    self.global_path_storage_full = True
                    print("global path 저장완료")
                elif self.global_path_storage_full == True:
                    self.target_control(200, 0)
                    if self.ego.speed<0.5:
                        self.first_stop = True
                        print('ready for parallel parking ')
            elif (self.first_stop == True) and (self.second_stop == False):
                if self.forward_tra_create == False:
                    self.plan.behavior_decision = "forward_trajectory_Create_para"
                    self.forward_tra_create = True #전진 경로 만들었다. 
                elif self.forward_tra_create == True: #전진 경로 만들었으니까 이제 할게?
                    # self.plan.behavior_decision = "parkingForwardOn"
                    self.plan.behavior_decision = "parking"
                    self.ego.target_gear = 0
                     ##'forward'
                    print('forward driving ')
                    if len(self.global_path.x) - 5 <= self.ego.index:
                        self.target_control(200,0) #브레이크 값 실험적 구해야 해요
                        if self.ego.speed<0.5:    
                            print('전진 종료')
                            self.second_stop = True
                    else:
                        if self.ego.index<=5:
                            self.target_control(0, 12)
                        else:
                            self.target_control(0, 10)
            elif (self.second_stop == True) and (self.third_stop == False):
                if self.backward_tra_create1 == False:
                    self.plan.behavior_decision = "backward_trajectory_Create_para"
                    self.backward_tra_create1 = True
                    print('경로 생성 완료!!!')
                elif self.backward_tra_create1 == True:
                    self.ego.target_gear = 2
                    if self.ego.index<=5:
                        self.target_control(0, 10)
                    else:
                        self.target_control(0, 5)
                    
                    if len(self.global_path.x) - (self.parking.hy1 + self.parking.hy2 + self.parking.hy3) <= self.ego.index <= len(self.global_path.x) - (self.parking.hy2 + self.parking.hy3) :
                        self.parking.on = 'on'
                        self.ego.target_steer = 27

                    elif self.ego.index<=len(self.global_path.x)-self.parking.hy3:
                            self.parking.on = 'on'
                            self.ego.target_steer = 0
                    elif self.ego.index<=len(self.global_path.x)-self.parking.hy3<=self.ego.index<=len(self.global_path.x)-1:
                        self.parking.on='on'
                        self.ego.target_steer=-27
                        if len(self.global_path.x)-15<=self.ego.index:
                            # self.target_control(200,0)
                            self.ego.input_brake = 200
                            self.ego.input_speed = 0
                            if self.ego.speed < 0.02:
                                self.third_stop= True
                                self.parking.on='off'
                                sleep(2)
                    else:
                        self.parking.on='off'       
            elif (self.third_stop ==True) and (self.fourth_stop ==False) :
                    if self.backward_tra_create2==False:    
                        self.plan.behavior_decision="exit"
                        self.backward_tra_create2=True
                    elif self.backward_tra_create2:
                        self.plan.behavior_decision = "parkingFowardOn"
                        self.ego.target_gear = 0
                        self.target_control(0, 5)
                        if self.ego.index >= len(self.global_path.x)-20:                           
                            self.target_control(20,0)
                            self.parking_create=True
                            self.fourth_stop=True
            else:
               pass
        else: # 원래대로 주행
            self.trans_global_path(self.global_path_storage_x,self.global_path_storage_y)
            self.shared.plan.behavior_decision == "go"
            self.plan.state = "go"
            self.target_control(0,10)

    def parking_parallel_jm(self):
        if not self.first_stop and 3650 <= self.ego.index: # stop
            print("step 1")
            self.target_control(200, 0)
            if self.ego.speed<0.5:
                self.first_stop = True
                sleep(0.2)

        elif self.first_stop and not self.second_stop: # go little
            self.ego.target_gear = 2
            if self.ego.target_gear == 2:
                self.second_stop = True
            # print("step 2")
            # if self.ego.index < 3690:
            #     self.target_control(0,5)
            # else:
            #     self.target_control(200,0)
            #     if self.ego.speed<0.5:    
            #         self.second_stop = True
            #         self.ego.target_gear = 2
            #         sleep(1)

        elif self.second_stop and not self.third_stop: # first turn
            print("step 3")
            if abs(self.ego.heading-305)>10:
                self.parking.on='on'
                self.ego.target_steer = 27
                self.target_control(0,5)
            else:
                self.target_control(200,0) 
                if self.ego.speed<0.5:    
                    self.third_stop = True
                    sleep(0.2)
        
        elif self.third_stop and not self.fourth_stop: # go little
            # print("step 4")
            left_point = np.array([72.9, 80])
            right_point = np.array([74.8, 83])
            ego_point = np.array([self.ego.x, self.ego.y])
            vec1 = (left_point[0]-right_point[0], left_point[1]-right_point[1], 0)
            vec2 = (ego_point[0]-right_point[0], ego_point[1]-right_point[1], 0)
            print("step 4. result : ", np.round(np.cross(vec1, vec2)[2],1))
            if np.cross(vec1, vec2)[2] > 0:
                self.ego.target_steer = 0
                self.target_control(0,4)
            else:
                self.target_control(200,0)
                if self.ego.speed<0.5:    
                    self.fourth_stop = True
                    sleep(0.2)
        
        elif self.fourth_stop and not self.fifth_stop: # second turn
            print("step 5")
            if abs(self.ego.heading-241)>10:
                self.ego.target_steer = -27
                self.target_control(0,4)
            else:
                self.ego.target_steer = 0
                self.target_control(200,0)
                if self.ego.speed<0.5:
                    self.fifth_stop = True

        elif self.fifth_stop and not self.sixth_stop: # stop
            print("step 6")
            if self.ego.index > 3620:
                self.target_control(0,5)
            else:
                self.target_control(200,0)
                if self.ego.speed<0.5:
                    self.sixth_stop = True
                    sleep(0.2)

        elif self.sixth_stop and not self.seventh_stop: # go forward
            print("step 7")
            self.ego.target_gear = 0
            if abs(self.ego.heading-305)>10:
                self.ego.target_steer = -27
                self.target_control(0,4)
            else:
                self.target_control(200,0)
                if self.ego.speed<0.5:
                    self.seventh_stop = True
                    self.target_control(0,0)
                    sleep(0.2)
        
        elif self.seventh_stop and not self.eighth_stop: # finish
            print("step 8")
            self.target_control(0,4)
            self.parking.on = "off"
            self.plan.state = "go"

        else:
            pass

    ###########################################################
    def obstacle_avoidance(self):
        '''
        motion.py에 만들어 놓은 all_obstacle_avoidance를 호출.
        obstacle_avoidance는 회피주행이 예상되는 index에서 발견되기 때문에
        실질적으로 장애물이 없어도 돌아가는 function.

        따라서 인지 데이터에서 장애물이 없으면 behavior_decision을 obstacle_avoidance로
        바꿀 필요가 없음.
        '''
        self.plan.behavior_decision = "obstacle_avoidance"
        

   ##################################################################################
    # def static_obstacle(self):
    #     self.plan.behavior_decision = "static_obstacle_avoidance"
    #     index = len(self.perception.objx)
        
    #     if (self.range(2175,50)) and self.obstacle_stop == False:
    #         self.target_control(100,0)
    #         sleep(3)
    #         self.target_control(0,10)
    #         self.obstacle_stop = True

    #     if (len(self.perception.objx) > 0):
    #         self.obs_dis = 15.5
    #         for i in range(0, index):
    #             self.dis = sqrt(
    #                 (self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
    #             self.obs_dis = min(self.obs_dis, self.dis)
    #             print(len(self.perception.objx), " ", self.obs_dis)

    #         if self.obs_dis <= 10:
    #             self.target_control(0, 5)
    #             self.obstacle_checker = True
    #             self.time_checker = False
                
    #     elif self.obstacle_checker == True:
    #         if self.time_checker == False:
    #             self.cur_t = time()
    #             self.time_checker = True
    #         if time() - self.cur_t < 3:
    #             self.target_control(0, 5)
    #         else:
    #             self.target_control(0, 7)
            
    #     else:
    #         self.target_control(0, 7)

    def turn_left(self):
        if self.perception.tleft == 1 or self.perception.tgreen == 1:
            self.plan.behavior_decision = "go"
            self.target_control(0, self.speed)
        else:
            if self.range(1610, 85):
                self.plan.behavior_decision = "stop"
                self.target_control(100, 0)
            else:
                self.plan.behavior_decision = "go"
                self.target_control(0, self.speed)

    def emergency_stop(self):
        self.target_control(0, 10)
        self.plan.behavior_decision = "emergency_avoidance"
        if self.shared.plan.obstac == True:
            self.target_control(150, 0)
            sleep(3)
            self.target_control(0, 10)
