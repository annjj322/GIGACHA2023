from math import hypot, cos, sin, degrees, atan2, radians, pi, sqrt
import numpy as np
class LatController():
    def __init__(self, eg, sh, lattice, pl, park):
 
        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = park
        self.lattice_path = lattice

        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        self.k = 0.55#1.5
        self.lookahead_default = 2 #look-ahead default 
        self.old_nearest_point_index=None
        # self.current_point_index = None
        
    def run(self):
        while(1):
            try:
                if self.parking.on == "on":
                    self.parking_run()
                elif self.parking.on == "forced":
                    self.parking_run2()
                elif self.parking.on == "U_turn":
                    self.U_turn()
                elif self.parking.on == "off":
                    self.path = self.lattice_path[self.shared.selected_lane]
                    Lf = min(self.k * self.ego.speed + self.lookahead_default, 6)
                    target_index = len(self.path.x) - 49
                    tx = self.path.x[target_index]
                    ty = self.path.y[target_index]
                    alpha = (np.radians(self.ego.heading) - atan2(ty - self.ego.y, tx - self.ego.x))
                    steer = np.degrees(atan2(2.0 * self.ego.WB * sin(alpha) / Lf, 1.0)) 
                    steer = np.clip(steer, -27.0, 27.0)
                    if degrees(angle) < 0.5 and degrees(angle) > -0.5:
                        angle = 0        
                    if abs(steer) > 5: 
                        Lf *=0.5
                        steer *= 0.8
                    self.steer = steer

                return self.steer

            except IndexError:
                print("++++++++lat_controller+++++++++")
    
    def calc_distance(self, point_x, point_y):
        dx = self.ego.x - point_x
        dy = self.ego.y - point_y
        d= np.hypot(dx,dy)
        return d
        
    
        
    # def search_target_index(self): #지용이
    #     # d = []
    #     # if self.current_point_index is None:
    #     #     for i in range(len(self.global_path.x)):
    #     #         dx = [self.ego.x - self.global_path.x[i]] # pure pursuit: state.rear_x - cx[i]를 리스트로 저장
    #     #         dy = [self.ego.y - self.global_path.y[i]] # pure pursuit: state.rear_y - cy[i]를 리스트로 저장
    #     #         d.append(np.hypot(dx, dy)) # math.hypot은 인자 두개로 피타고라스 조져버리고 값 반환함
    #     #     d=np.hypot(dx,dy)
    #     #     ind = np.argmin(d) # ind = np.argmin(d) # np.argmin([list])는 리스트의 최솟값의 index를 반환함
    #     if self.current_point_index is None:
    #         dx= [self.ego.x - icx for icx in self.global_path.x]
    #         dy= [self.ego.y - icy for icy in self.global_path.y]    
    #         d = np.hypot(dx, dy) # math.hypot은 인자 두개로 피타고라스 조져버리고 값 반환함

    #         ind = np.argmin(d)
    #         self.current_point_index = ind
    #         self.line_index.x = self.global_path.x[ind:]
    #         self.line_index.y = self.global_path.y[ind:]
            
    #     else:        
    #         self.line_index.x = self.global_path.x[ind:]
    #         self.line_index.y = self.global_path.y[ind:]
    #         ind=10
            
    #         # while len(line_index_x) < 1:
    #         #     if self.calc_distance(line_index_x[0],line_index_y[0]) > self.calc_distance(line_index_x[1],line_index_y[1]):
    #         #         del line_index_x[0]
    #         #         del line_index_y[0]
    #         #         #line_index_x = line_index_x.pop(0)
    #         #         #line_index_y = line_index_y.pop(0)
    #         #     else:
    #         #         break
        
    #     Lf = 10#self.k * self.ego.speed + self.lookahead_default
    #     # while Lf > self.calc_distance(line_index_x[0], line_index_y[0]):
    #     #     if (ind + 1) >= len(self.global_path.x): # final goal
    #     #         break  # not exceed goal
        
    #     return ind, Lf

    # def PurePursuit(self):
    #     self.path = self.lattice_path[self.shared.selected_lane]
    #     Lf = min(self.k * self.ego.speed + self.lookahead_default, 6)
    #     target_index = len(self.path.x) - 49
    #     tx = self.path.x[target_index]
    #     ty = self.path.y[target_index]
    #     alpha = (np.radians(self.ego.heading) - atan2(ty - self.ego.y, tx - self.ego.x))
    #     steer = np.degrees(atan2(2.0 * self.ego.WB * sin(alpha) / Lf, 1.0)) 
    #     steer = np.clip(steer, -27.0, 27.0)
    #     if degrees(angle) < 0.5 and degrees(angle) > -0.5:
    #         angle = 0        
    #     if abs(steer) > 5: 
    #         Lf *=0.5
    #         steer *= 0.8

    #     '''
    #     print("--------------------VALUES-----------------------")
    #         print("\nLf : ", Lf,"\n\n\n")
    #         print("TARGET ind : ", ind)
    #         print('EGO index : ', self.shared.ego.index, "\n")
    #         print("Lookahead : ", ind - self.shared.ego.index, '\n\n\n')
    #         print('EGO speed : {0:.2f}'.format(self.ego.speed))
    #         print("self.shared.ego.speed", self.shared.ego.speed)
    #         print('Input Speed : ', self.shared.ego.input_speed,"\n\n\n")
    #         print('Input Steer : {0:.2f}'.format(self.shared.ego.input_steer), "\n\n")
    #         print('heading : {:.2f}'.format(self.shared.ego.heading),"\n")
    #         print("heading_not shared : {:.2f}".format(self.shared.ego.heading),"\n")
    #         print("-------------------------------------------------")
    #     '''

    #     return steer

    # def PurePursuit(self):

    #     heading = self.ego.heading

    #     ################## !!!!  wrong 유심히 볼 것 !!!! #########################
    #     # self.rear_x = self.ego.x - ((self.WB/2) * cos(np.radians(heading)))
    #     # self.rear_y = self.ego.y - ((self.WB/2) * sin(np.radians(heading)))
    #     # feedback
    #     ########################################################################
    #     self.rear_x = self.ego.x # gps 센서의 위치는 뒷바퀴 축에 있음. 만약 그렇지 않다면, 기하학적으로 계산하면 됨.
    #     self.rear_y = self.ego.y

    #     ind, Lf = self.search_target_index() # trajectory에 target_course, 여기에 search_target_index 함수 적용. 이 때 현재 상태(state)를 기준으로함.     #i.e. 아래 main()에서 197번 줄 반복문을 통해 위의 Lf = k * state.v + Lfc값을 갱신하고, ind를 계속 찾는 역할을 함
    #     #if pind >= ind: # pind에 target_ind, 현재 계산된 인덱스(ind)가 더 앞쪽에 있을 때만 바꾼다 이 소리(즉, 현재 ind가 과거 어떤 지점의 ind보다 작으면 굳이 바꾸지 않음. <- 바꾸면 역행함.)
    #         #ind = pind # i.e. 비교 후 인덱스를 둘 중 다음(큰) 것으로 갱신

    #     #ind = self.ego.index + 50
    #     #Lf = 10
     
        
    #     tx = self.global_path.x[ind] #i.e. tx = target_course.cx[ind], tx는 현재 가는 바라본 곳의 x좌표
    #     ty = self.global_path.y[ind] # 바라본 곳의 y좌표
    #     #Lf = int(self.k * self.ego.speed + self.lookahead_default)
    #     #tx = self.global_path.x[self.ego.index + Lf] #+ self.ego.x
    #     #ty = self.global_path.y[self.ego.index + Lf] #+ self.ego.y
        
    #     alpha = (np.radians(heading) - atan2(ty - self.rear_y, tx - self.rear_x)) # 기하학적 관계식
    #     steer = np.degrees(atan2(2.0 * self.WB * sin(alpha) / Lf, 1.0)) #pure pursuit 알고리즘에 의한 식
        
        
      
        
    #     # brake_distance_ind = brake_distance * 10 # 1 index is 0.1 m = 10 cm. discard
    #     #######! gear: D = 0, N = 1, R = 2, P = 3?? 3 아닌 거 같은데
    #     ''' # LonController로 이동
    #     if self.ego.index >= 40: # 처음 시작 구간에서 브레이크 작동 방지. 만약 처음에 컨트롤러가 살아있는데 브레이크가 작동하여 가지 않는다면 이 코드를 유심히 봐야함. 거리가 너무 짧거나 인덱스가 너무 짧은 맵은 이 코드에 의해 오류가 생김. <- 거리 기준으로 하니 왕복코스에선 시작점이랑 거리가 비슷해져버려서 작동 안 하는 듯. 다시 인덱스 기준으로 롤백함. 실제 환경에선 극단적으로 짧은 인덱스는 없을 것 같음.
    #         if self.brake_distance_toggle == True:
    #             brake_distance = self.ego.speed/3.6 + 5 # [m] ## 급정거하면 이게 짧아져서 다시 가속하는 현상 있음. -> toggle 로 해결. 브레이크 작동하면 그 뒤론 제동거리 계산 및 업데이트 중단.
            
    #         if hypot(self.ego.x-self.global_path.x[-1], self.ego.y-self.global_path.y[-1]) <= brake_distance: #감속구간, brake_distance 는 실차 제동거리에 따라 조정
    #                 speed = 0
    #                 brake = 10 #100으로 하니까 급정거해서 그런지 통통 튀면서 멈춤. <- 아 급정거하니까 ego.speed가 값이 급격히 변하면서 brake_distance 가 급격히 감소하여 그런 거였음. -->>> 10 추천.
    #                 gear = 1 # N
    #                 self.brake_distance_toggle = not self.brake_distance_toggle # toggle 작동.
    #                 if self.ego.speed == 0:
    #                     gear = 1 #! 속도가 0이면 P 기어 넣기. 그런데 P 기어 입력값을 모르겠음. 그래서 일단 중립N 박음.

    #         else:
    #             speed = 15 # 시뮬레이터 상에서 최고속도는 24-25로 추정됨.
    #             brake = 0
    #             gear = 0 # D
    #     else:
    #         speed = 15 # 속도리미트 20으로 제한되어 있는 듯. 그건 어디서 제한 했는지 찾아야함. 20 이하 속도는 잘 설정됨. wasd로 직접 조작하면 25km까지 나옴.
    #         brake = 0
    #         gear = 0
    #     '''
    #     steer = np.clip(steer, -27.0, 27.0) # 시뮬레이터 상에서 최고 조향각도는 28.7로 추정됨.

    #     ###### 비상용 speed, brake, gear 값들. 종제어없이 const로 주행하기엔 무리 없음. 위의 코드가 만약 오류를 일으키는 것 같으면 위를 주석처리하고 아래를 활성화시켜 보면 됨.
    #     #speed = 20
    #     #brake = 0
    #     #gear = 0
    #     ######
    #     #steer = max(min(steer, 27.0), -27.0)
    #     if abs(steer) > 5: # [degree] 곡선 부드럽게 하는 코드
    #          Lf *=0.5
    #          steer *= 0.8

    #     # print("--------------------VALUES-----------------------")
    #     # print("\nLf : ", Lf,"\n\n\n")
    #     # print("TARGET ind : ", ind)
    #     # print('EGO index : ', self.shared.ego.index, "\n")
    #     # print("Lookahead : ", ind - self.shared.ego.index, '\n\n\n')
    #     # print('EGO speed : {0:.2f}'.format(self.ego.speed))
    #     # print("self.shared.ego.speed", self.shared.ego.speed)
    #     # print('Input Speed : ', self.shared.ego.input_speed,"\n\n\n")
    #     # print('Input Steer : {0:.2f}'.format(self.shared.ego.input_steer), "\n\n")
    #     # print('heading : {:.2f}'.format(self.shared.ego.heading),"\n")
    #     # print("heading_not shared : {:.2f}".format(self.shared.ego.heading),"\n")
    #     # print("-------------------------------------------------")
        
    #     return steer #, brake, gear # Lon_controller 로 옮김.
    #     # return steer, speed, brake, gear // speed 항을 배고 Lon에서 종제어 하도록 설정

    # Pure Pursuit 이지용


    # global_path            
    # def pure_pursuit(self):
    #     self.path = self.lattice_path[self.shared.selected_lane]
        
    #     # temp
    #     target_index = len(self.path.x) - 49
    #     # todo
    #     # lookahead = min(self.k * self.ego.speed + self.lookahead_default, 7)
    #     # target_index = int(lookahead * 10)
        
    #     target_x, target_y = self.path.x[target_index], self.path.y[target_index]
    #     target_distance = sqrt((target_x - self.ego.x)**2 + (target_y - self.ego.y)**2)
    #     target_angle = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360
    #     alpha = self.ego.heading - target_angle
    #     steer = atan2(2 * self.WB * sin(radians(alpha)) / target_distance, 1)
        
    #     if (degrees(steer) < 0.5 and degrees(steer) > -0.5):
    #         steer = 0
        
    #     self.steer = max(min(degrees(steer), 27.0), -27.0)
        
    #     return self.steer

    def parking_run(self):
        if self.parking.direction == 0:
            self.path = self.parking.forward_path
            lookahead = 5
        else:
            self.path = self.parking.backward_path
            lookahead = 5
        # if not self.parking.inflection_on:
        target_index = lookahead + self.parking.index
        # else:
        #     target_index = len(self.parking.backward_path.x) - 1

        target_x, target_y = self.path.x[target_index], self.path.y[target_index]
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

        heading = self.ego.heading
        ###### Back Driving ######
        if self.ego.target_gear == 2:
            heading += 180
            heading %= 360
        ##########################

        alpha = heading - tmp
        angle = atan2(2.0 * self.WB *
                      sin(radians(alpha)) / lookahead, 1.0)

        ###### Back Driving ######
        if self.ego.target_gear == 2:
            angle = -1.5*angle
        ##########################

        if degrees(angle) < 3.5 and degrees(angle) > -3.5:
            angle = 0

        self.steer = max(min(degrees(angle), 27.0), -27.0)

    def parking_run2(self):
        self.steer = self.ego.target_steer