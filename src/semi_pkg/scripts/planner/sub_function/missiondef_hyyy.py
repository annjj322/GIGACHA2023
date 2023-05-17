def Parking_KCity_parallel_hy(self):
        if (self.parking_create == False):
            if (3602 <= self.ego.index <= 3622) and self.first_stop == False: # K-City
                self.plan.behavior_decision = "stop"
                self.target_control(100, 0)
                sleep(2) #일단 주차 구간에 들어왔으니 멈출게?
                self.first_stop = True

            if (self.first_stop == True) and (self.second_stop == False):
                if self.forward_tra_create == False:
                    self.plan.behavior_decision = "forward_trajectory_Create"
                    self.forward_tra_create = True #전진 경로 만들었다. 
                elif self.forward_tra_create == True: #전진 경로 만들었으니까 이제 할게?
                    self.plan.behavior_decision = "parkingforwardOn"
                    self.ego.target_gear = 0
                    self.parking.on = "off"
                    self.target_control(0, 5)
                    # print("len: ", len(self.global_path.x))
                    # print("ego_ind: ", self.ego.index)
                    d=self.cal_cal(self.parking.forward_path.x[-1],self.parking.forward_path.y[-1])
                    if d<0.1:
                        self.target_control(100, 0) #전지해야할 곳 도착쓰
                        sleep(3) 
                        self.second_stop = True # 경로와 직선 사이 교점 근처에 정차
                        

            if (self.second_stop == True) and (self.third_stop == False):
                if self.backward_tra_create == False:
                    self.plan.behavior_decision = "backward_trajectory_Create"
                    self.backward_tra_create = True
                elif self.backward_tra_create == True:
                    self.plan.behavior_decision = "parkingbackwardOn"
                    self.ego.target_gear = 2
                    self.parking.on = "on"
                    self.target_control(0, 2)
                    print("len: ", len(self.global_path.x))
                    print("ego_ind: ", self.ego.index)
                    d1=self.cac_cal(self.parking.backward_path.x[-1],self.parking.backward_path.y[-1])
                    if d<0.1:
                        self.target_control(100, 0)
                        sleep(3) 
                        self.third_stop = True # 평행 주차 성공
            else:
                self.plan.state = "go"
def cal_cal(self,x,y):
    dx=self.ego_info_x-x
    dy=self.ego_info_y-y
    d=math.hypot(dx,dy)
    return d