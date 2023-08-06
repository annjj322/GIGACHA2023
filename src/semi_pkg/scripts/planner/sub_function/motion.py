from time import sleep
import numpy as np
from shared.path import Path
from .cubic_spline_planner import calc_spline_course
from math import hypot,atan2,sin,cos,pi
# import math as m
import threading
# import rospy
# from nav_msgs.msg import Path as Path2
import threading
class Potential_field:
    def __init__(self, ego):
        self.repulsive = 0
        self.attractive = 0
        self.potential = 0

        self.vehicle_position = None
        self.goal_position = None
        self.obstacles = None

        # for visualization
        self.repulsive_scale = 0 
        self.attractive_scale = 0
        self.potential_scale = 0

        self.ego = ego
        self.pf_lock = threading.Lock()

    def update(self, vehicle_position, goal_position, obstacles):
        self.repulsive = 0
        self.attractive = 0
        self.potential = 0

        self.vehicle_position = vehicle_position
        self.goal_position = goal_position
        self.obstacles = obstacles
        
    # 척력장 계산
    def calculate_repulsive_field(self):
        repulsive = 0
        repulsive_scale = 0 
        
        for obstacle in self.obstacles:
            distance = np.linalg.norm(self.vehicle_position - obstacle)
            distance = max(distance-1.5,0.01)
            ###
            scale = 7/distance
            ###

            unit_vector = (self.vehicle_position - obstacle)/distance**1.3

            # inv_inc = [-0.89454132, 0.44698527]

            
            # unit_vector = np.dot(unit_vector, inv_inc) * np.array(inv_inc)
            

            # print("repulsive unit vec:", unit_vector)
            repulsive += unit_vector * scale
            repulsive_scale += scale
            # print("repulsive", repulsive)
        return repulsive, repulsive_scale
    
    def calculate_attractive_field(self):
        distance = np.linalg.norm(self.vehicle_position - self.goal_position)
        distance += 0.01
        ###
        scale = 15
        ###

        unit_vector = (self.goal_position - self.vehicle_position)/distance
        # print("attractive unit vec : ", unit_vector)
        attractive = unit_vector * scale
        attractive_scale = scale
        # print("attractive", attractive)

        return attractive, attractive_scale
    
    def calculate_potential_field(self, repulsive, repulsive_scale, attractive, attractive_scale):
        self.potential = repulsive + attractive

        # for erp42 : constant speed
        self.potential = self.potential/np.linalg.norm(self.potential)
        scale = 0.1
        self.potential = self.potential*scale

        self.potential_scale = repulsive_scale + attractive_scale
     

    def run(self):
        self.pf_lock.acquire()
        repulsive, rep_scale = self.calculate_repulsive_field()
        attractive, att_scale = self.calculate_attractive_field()
        self.calculate_potential_field(repulsive, rep_scale, attractive, att_scale)
        self.pf_lock.release()

    

class Motion():
    def __init__(self, sh, pl, eg, pk):
        self.shared = sh
        self.plan = pl
        self.ego = eg
        self.parking = pk

        self.global_path = self.shared.global_path # from localizer

        # step
        self.first_stop = False
        self.second_stop = False
        self.third_stop = False
        self.fourth_stop = False
        self.fifth_stop = False
        self.sixth_stop = False
        self.seventh_stop = False
        self.eighth_stop = False
        self.ninth_stop = False
        self.tenth_stop = False
        self.eleventh_stop = False
        self.twelfth_stop = False
        self.thirteenth_stop = False

        # parking
        self.Ledgedata = [64.6268, 42.5435] # kcity parking space
        self.Redgedata = [65.5141, 40.1389]
        self.middlepoint = [(self.Ledgedata[0] + self.Redgedata[0])/2,(self.Ledgedata[1] + self.Redgedata[1])/2]
        dest_x, dest_y = self.find_destination()
        self.destination = [dest_x, dest_y]
        self.path_storage_x = []
        self.path_storage_y = []
        self.L = 1.04
        # self.R = self.L/sin(radians(27))
        self.R = 3
        # self.d = sqrt((self.ego[0] - self.middlepoint[0])**2 + (self.ego[1] - self.middlepoint[1])**2)
        self.global_path_storage_full = False

    
        # delivery
        self.delivery_point = None
        self.delivery_index = None
        self.add = 50

        # for save global path
        self.global_path_x_storage = []
        self.global_path_y_storage = []
        
        # pa
        self.obstacles=[]
        self.first_flag=False
        self.inc=0
        self.k=threading.Lock()
        self.gp_save_flag=False
        self.x=[]
        self.y=[]
        self.WB=1.04
        self.local_path = self.shared.local_path
        self.hy_test = self.shared.hy_test
        
        # obstacle avoidance
        self.flag = True
        self.invisible_wall2=[]
        self.tmp_vehicle_position = None
        self.invisible_wall()
        self.jiamtong = []
        self.ego_trace= []
        self.prev=0
    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed
    
    def nearest_index(self, pointx, pointy):
        dist = []
        dx = [pointx - x for x in self.global_path.x[0:-1]]
        dy = [pointy - y for y in self.global_path.y[0:-1]]
        for i in range(len(dx)):
            distx = dx[i]
            disty = dy[i]
            dist.append(np.hypot(distx, disty))

        ind = int(np.argmin(dist))
        
        return ind

    def go(self):
        pass

#############################################################################################

    def parrallel_step1(self):
        if not self.first_stop and 3650 <= self.ego.index: # stop
            print("step 1")
            self.target_control(200, 0)
            if self.ego.speed<0.5:
                self.first_stop = True
                sleep(0.2)
                
    def parrallel_step2(self):
        if self.first_stop and not self.second_stop: # go little
            print("step 2")
            self.ego.target_gear = 2
            if self.ego.target_gear == 2:
                self.second_stop = True

    def parrallel_step3(self): 
        if self.second_stop and not self.third_stop: # first turn
            print("step 3")
            if abs(self.ego.heading-305)>10:
                self.parking.on='on1'
                self.ego.target_steer = 27
                self.target_control(0,5)
            else:
                self.target_control(200,0) 
                if self.ego.speed<0.5:    
                    self.third_stop = True
                    sleep(0.2)

    def parrallel_step4(self):
        if self.third_stop and not self.fourth_stop: # go little
            print("step 4")
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

    def parrallel_step5(self):
        if self.fourth_stop and not self.fifth_stop: # second turn
            print("step 5")
            if abs(self.ego.heading-241)>10:
                self.ego.target_steer = -27
                self.target_control(0,4)
            else:
                self.ego.target_steer = 0
                self.target_control(200,0)
                if self.ego.speed<0.5:
                    self.fifth_stop = True
                    
    def parrallel_step6(self):
        if self.fifth_stop and not self.sixth_stop: # stop
            print("step 6")
            if self.ego.index > 3620:
                self.target_control(0,5)
            else:
                self.target_control(200,0)
                if self.ego.speed<0.5:
                    self.sixth_stop = True
                    sleep(0.2)
    
    def parrallel_step7(self):
        if self.sixth_stop and not self.seventh_stop: # go forward
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

    def parrallel_step8(self):
        if self.seventh_stop and not self.eighth_stop: # finish
            print("step 8")
            self.target_control(0,4)
            self.parking.on = "off"
            self.plan.behavior_decision = "go"

#####################################################################################################

    def find_contact(self, ps, pf):
        # find global line
        global_inclination = (ps[1] - pf[1])/(ps[0] - pf[0])
        global_intercept = -global_inclination*ps[0] + ps[1]

        # find vertical line
        pl_inclination = (self.Ledgedata[1] - self.Redgedata[1])/(self.Ledgedata[0] - self.Redgedata[0])
        vertical_inclination = -1/pl_inclination
        vertical_intercept = -vertical_inclination*self.middlepoint[0] + self.middlepoint[1]

        # find contact point
        cont_x = (global_intercept - vertical_intercept)/(vertical_inclination - global_inclination)
        cont_y = vertical_inclination*cont_x + vertical_intercept

        return cont_x, cont_y
    
    def find_destination(self):
        pl_inclination_angle = self.find_inclination_angle(self.Ledgedata, self.Redgedata)
        vertical_inclination_angle = pl_inclination_angle - pi/2

        dest_x = self.middlepoint[0] + 2*cos(vertical_inclination_angle)
        dest_y = self.middlepoint[1] + 2*sin(vertical_inclination_angle)

        return dest_x, dest_y
    
    def making_forward_path(self): 

        ''' 최소회전반경을 고려한 주차 코스 짜기 - 차량과 주차공간이 가까울 때, 멀 때로 구분하였음 '''

        incline_angle1 = self.find_inclination_angle(self.Ledgedata, self.Redgedata) # 인지한 주차공간의 두 점 기울기 각도 찾기 (rad)
        print("angle1: ", np.degrees(incline_angle1))
        ps = [self.global_path.x[self.ego.index - 1], self.global_path.y[self.ego.index - 1]]
        pf = [self.global_path.x[self.ego.index + 1], self.global_path.y[self.ego.index + 1]]

        incline_angle2 = self.find_inclination_angle(pf, ps) 
        # incline_angle2 = self.find_inclination_angle(ps, pf) 
        print("asdf:", np.degrees(incline_angle2))
        incline_angle2 = pi/2 + incline_angle2 # global path의 수직 기울기 각도 찾기 (rad)
        print("angle2: ", np.degrees(incline_angle2))
        fan_angle = incline_angle2 - incline_angle1

        vect1_size = abs(np.sqrt((self.Ledgedata[0]-self.Redgedata[0])**2 + (self.Ledgedata[1]-self.Redgedata[1])**2)) 
        vect1 = [(self.Redgedata[0]-self.Ledgedata[0])/vect1_size, (self.Redgedata[1]-self.Ledgedata[1])/vect1_size] # 주차공간의 두 점 사이를 잇는 단위벡터
        # vect1 = [cos(incline_angle1), sin(incline_angle1)] # 주차공간의 두 점 사이를 잇는 단위벡터
        circle_center = [self.middlepoint[0]+self.R*vect1[0], self.middlepoint[1]+self.R*vect1[1]] # 원 중심 찾기

        # find global line
        a1 = (ps[1] - pf[1])/(ps[0] - pf[0]) # global path 기울기
        b1 = -a1*ps[0] + ps[1] # global path 선분에 대한 식

        # find vertical line
        a2 = -1/a1 # global path와 수직인 선의 기울기
        b2 = -a2*circle_center[0] + circle_center[1] # 위 기울기를 가지면서 점 pO를 지나는 선분에 대한 식

        # find contact point
        cont_x = (b2 - b1)/(a1 - a2) # 위 두 선분이 만나는 지점의 x 좌표 -> 즉 이 좌표는 global path 상에 놓여있다
        cont_y = a1*cont_x + b1 # 위 두 선분이 만나는 지점의 y 좌표 -> 즉 이 좌표는 global path 상에 놓여있다

        # find vector
        vect2_size = np.sqrt((cont_x - circle_center[0])**2 + (cont_y - circle_center[1])**2) # pO 점부터 위에서 구한 점 사이를 잇는 벡터의 사이즈
        vect2 = [(cont_x - circle_center[0])/vect2_size, (cont_y - circle_center[1])/vect2_size] # 위에서 구한 벡터의 단위 벡터 (크기 = 1)
        
        fan_start_point = [circle_center[0]+self.R*vect2[0], circle_center[1]+self.R*vect2[1]] # 차량이 최소회전반경을 돌도록 하는 시작 지점 찾기
        
        self.fan_path_x, self.fan_path_y = self.generate_fan_paths(self.R, fan_angle, circle_center[0], circle_center[1], fan_start_point[0], fan_start_point[1], self.middlepoint[0], self.middlepoint[1]) # 위에서 구한 시작지점부터 주차공간까지 잇는 부채꼴 모양의 경로

        back_vect_size = abs(np.sqrt((ps[0]-pf[0])**2 + (ps[1]-pf[1])**2)) # 시작지점부터 출발하면 오차가 존재할 수 있으므로 뒤 3m부터 출발하여 직선으로 가다가 원을 그리며 주차하도록 함
        back_vect = [(ps[0] - pf[0])/back_vect_size, (ps[1] - pf[1])/back_vect_size] # global path 역방향의 단위 벡터 (크기 = 1)
        back_point = [fan_start_point[0] + 5*back_vect[0], fan_start_point[1] + 5*back_vect[1]] # 시작지점에서 3m 뒤로 간 후 시작할 것
        
        straight_path_x1 = [back_point[0], fan_start_point[0]] 
        straight_path_y1 = [back_point[1], fan_start_point[1]]
        self.straight_path_x1, self.straight_path_y1, cyaw, ck, s = calc_spline_course(straight_path_x1, straight_path_y1) # 그 3m 경로를 만들어줌

        final_straight_x= [self.middlepoint[0], self.destination[0]]
        final_straight_y=[self.middlepoint[1], self.destination[1]]
        self.final_straight_x, self.final_straight_y, cyaw, ck, s = calc_spline_course(final_straight_x, final_straight_y) # 주차공간으로의 안착을 위한 추가적인 경로

        a = a1
        b = -1
        c = -a*self.middlepoint[0]+self.middlepoint[1]
        self.d = abs(a*self.ego.x+b*self.ego.y+c)/np.sqrt(a**2+b**2)
        if self.d < self.R*(1-cos(fan_angle)):

            ''' 차량과 주차공간이 가까울 때 '''

            print("distance is short")
            print("d: ", self.d)
            print("groundtruth: ", self.R*(1-cos(fan_angle)))
            print("alpha: ", np.degrees(fan_angle))
            path_x = self.straight_path_x1 + self.fan_path_x + self.final_straight_x
            path_y = self.straight_path_y1 + self.fan_path_y + self.final_straight_y

            StartEndPath_x, StartEndPath_y = path_x, path_y

        else:

            ''' 차량과 주차공간이 충분히 멀거나 최소회전반경에 딱 맞을 때 '''

            print("distance is long")
            print("d: ", self.d)
            print("groundtruth: ", self.R*(1-cos(fan_angle)))
            ps2 = [fan_start_point[0] + back_vect[0], fan_start_point[1] + back_vect[1]]
            pf2 = [fan_start_point[0] - back_vect[0], fan_start_point[1] - back_vect[1]]
            cont_x2, cont_y2 = self.find_contact(ps2, pf2)

            ps3 = [self.ego.x + back_vect[0], self.ego.y + back_vect[1]]
            pf3 = [self.ego.x - back_vect[0], self.ego.y - back_vect[1]]
            cont_x3, cont_y3 = self.find_contact(ps3, pf3)

            path_x = self.straight_path_x1 + self.fan_path_x
            path_y = self.straight_path_y1 + self.fan_path_y

            vect3 = [cont_x3 - cont_x2, cont_y3 - cont_y2]
            path_x = [pointx + vect3[0] for pointx in path_x]
            path_y = [pointy + vect3[1] for pointy in path_y]

            straight_path_x2 = [path_x[-1], self.middlepoint[0]]
            straight_path_y2 = [path_y[-1], self.middlepoint[1]]
            self.straight_path_x2, self.straight_path_y2, cyaw, ck, s = calc_spline_course(straight_path_x2, straight_path_y2) # 부채꼴 모양의 경로 끝지점에서 주차공간까지 잇는 직선

            path_x = path_x + self.straight_path_x2 + self.final_straight_x
            path_y = path_y + self.straight_path_y2 + self.final_straight_y
            
            StartEndPath_x, StartEndPath_y = path_x, path_y

        return StartEndPath_x, StartEndPath_y

    def generate_fan_paths(self, radius, angle, Ox, Oy, fan_start_pointx, fan_start_pointy, end_pointx, end_pointy, ds=0.1):
        paths_x = []
        paths_y = []
        num_points = int(np.ceil(angle / ds))

        start_angle = atan2(fan_start_pointy - Oy, fan_start_pointx - Ox)
        end_angle = atan2(end_pointy - Oy, end_pointx - Ox)

        if start_angle <= end_angle:
            while start_angle <= end_angle:
                x = round(Ox + radius * cos(start_angle), 2)
                y = round(Oy + radius * sin(start_angle), 2)

                paths_x.append(x)
                paths_y.append(y)

                start_angle += angle / num_points
                start_angle = round(start_angle, 2)
        else:
            while start_angle >= end_angle:
                x = round(Ox + radius * cos(start_angle), 2)
                y = round(Oy + radius * sin(start_angle), 2)

                paths_x.append(x)
                paths_y.append(y)

                start_angle -= angle / num_points
                start_angle = round(start_angle, 2)

        return paths_x, paths_y        

    def find_inclination_angle(self, p1, p2):
        inclination_angle = atan2((p1[1] - p2[1]),(p1[0] - p2[0]))
        inclination_angle = np.degrees(inclination_angle)
        inclination_angle = (inclination_angle + 360)%360

        return np.radians(inclination_angle)

    def making_reverse_forward_path(self):
        self.global_path.x, self.global_path.y = list(reversed(self.global_path.x)), list(reversed(self.global_path.y))  
        return self.global_path.x, self.global_path.y

    def making_backward_path(self):
        ps = [self.global_path.x[self.ego.index - 1], self.global_path.y[self.ego.index - 1]]
        pf = [self.global_path.x[self.ego.index + 1], self.global_path.y[self.ego.index + 1]]
        
        cont_x, cont_y = self.find_contact(ps, pf)

        cont_ind = self.nearest_index(cont_x, cont_y) # 교차점의 index

        incline_angle1 = self.find_inclination_angle(self.Ledgedata, self.Redgedata) # 인지한 주차공간의 두 점 기울기 각도 찾기 (rad)


        incline_angle2 = self.find_inclination_angle(ps, pf) 
        incline_angle2 = pi/2 + incline_angle2 # global path의 기울기 각도 찾기 (rad)

        fan_angle = abs(incline_angle1 - incline_angle2)

        a1 = (ps[1] - pf[1])/(ps[0] - pf[0])
        a = a1
        b = -1
        c = -a*self.middlepoint[0]+self.middlepoint[1]
        self.d = abs(a*self.ego.x+b*self.ego.y+c)/np.sqrt(a**2+b**2)
        if self.d < self.R*(1-cos(fan_angle)):
            distance = 15 # 주차공간과 가까우면 10m 뒤로 가서 충분한 거리 확보
        else:
            distance = 10  # 주차공간과 먼 경우는 크게 중요치 않다.

        back_vect_size = abs(np.sqrt((ps[0]-pf[0])**2 + (ps[1]-pf[1])**2)) # 시작지점부터 출발하면 오차가 존재할 수 있으므로 뒤 3m부터 출발하여 직선으로 가다가 원을 그리며 주차하도록 함
        back_vect = [(ps[0] - pf[0])/back_vect_size, (ps[1] - pf[1])/back_vect_size] # global path 역방향의 단위 벡터 (크기 = 1)
        back_point1 = [self.ego.x + 100*back_vect[0], self.ego.y + 100*back_vect[1]] 

        backward_path_x1 = [self.ego.x, back_point1[0]]
        backward_path_y1 = [self.ego.y, back_point1[1]]

        backward_path_x1, backward_path_y1, cyaw, ck, s = calc_spline_course(backward_path_x1, backward_path_y1)
        dist = []
        dx = [cont_x - x for x in backward_path_x1[0:-1]]
        dy = [cont_y - y for y in backward_path_y1[0:-1]]
        for i in range(len(dx)):
            distx = dx[i]
            disty = dy[i]
            dist.append(hypot(distx, disty))
        back_cont_ind = int(np.argmin(dist))
        
        back_point2 = [backward_path_x1[back_cont_ind] + distance*back_vect[0], backward_path_y1[back_cont_ind] + distance*back_vect[1]] # 교차점으로부터 몇 m 뒤로 간 후 시작할 것

        backward_path_x2 = [self.ego.x, back_point2[0]]
        backward_path_y2 = [self.ego.y, back_point2[1]]
        
        backward_path_x, backward_path_y, cyaw, ck, s = calc_spline_course(backward_path_x2, backward_path_y2)

        return backward_path_x, backward_path_y

    def diagonal_step1(self):
        if not self.first_stop and 555 <= self.ego.index: # stop
        # if (len(self.shared.perception.edge_L) != 0) and (self.first_stop == False): # K-City
            self.parking.on='on'
            print("step 1")
            if self.global_path_storage_full == False:
                self.global_path_storage_x = self.global_path.x
                self.global_path_storage_y = self.global_path.y
                self.global_path_storage_full = True
            elif self.global_path_storage_full == True:
                self.target_control(100, 0)
                if self.ego.speed<0.5:
                    self.first_stop = True
                    sleep(0.2)

    def diagonal_step2(self):
        if self.first_stop and not self.second_stop: # make path
            print("step 2")
            self.global_path.x, self.global_path.y = self.making_backward_path()
            self.second_stop = True
            sleep(0.2)

    def diagonal_step3(self):
        if self.second_stop and not self.third_stop: # backward
            print("step 3")
            self.ego.target_gear = 2
            if self.ego.target_gear == 2:
                self.third_stop = True
                sleep(0.2)
                
    def diagonal_step4(self):
        if self.third_stop and not self.fourth_stop: # 
            print("step 4")
            self.target_control(0, 5)
            if self.ego.index >= len(self.global_path.x)-100:
                self.target_control(100, 0)
                self.global_path.x = self.global_path_storage_x # 다시 원래 경로
                self.global_path.y = self.global_path_storage_y
                self.fourth_stop = True # 경로와 직선 사이 교점 근처에 정차
                sleep(0.2)

    def diagonal_step5(self):
        if self.fourth_stop and not self.fifth_stop: # 
            print("step 5")
            self.global_path.x, self.global_path.y = self.making_forward_path()
            self.fifth_stop = True
            sleep(0.2)

    def diagonal_step6(self):
        if self.fifth_stop and not self.sixth_stop: # backward
            print("step 6")
            self.ego.target_gear = 0
            if self.ego.target_gear == 0:
                self.sixth_stop = True
                sleep(0.2)

    def diagonal_step7(self):
        if self.sixth_stop and not self.seventh_stop: # 
            print("step 7")
            self.target_control(0, 6)
            if self.ego.index >= len(self.global_path.x)-10:
                self.target_control(100, 0)
                if self.ego.speed<0.5:
                    self.seventh_stop = True
                    sleep(0.2)

    def diagonal_step8(self):
        if self.seventh_stop and not self.eighth_stop:
            print("step 8")
            self.global_path.x, self.global_path.y = self.making_reverse_forward_path()
            self.eighth_stop = True
            sleep(0.2)

    def diagonal_step9(self):
        if self.eighth_stop and not self.ninth_stop: # backward
            print("step 9")
            self.ego.target_gear = 2
            if self.ego.target_gear == 2:
                self.ninth_stop = True
                sleep(0.2)

    def diagonal_step10(self):
        if self.ninth_stop and not self.tenth_stop: # 
            print("step 10")
            self.target_control(0, 6)
            if self.ego.index >= len(self.global_path.x)-10:
                self.target_control(100, 0)
                self.global_path.x = self.global_path_storage_x # 다시 원래 경로
                self.global_path.y = self.global_path_storage_y
                self.tenth_stop = True # 경로와 직선 사이 교점 근처에 정차
                sleep(0.2)

    def diagonal_step11(self):
        if self.tenth_stop and not self.eleventh_stop: # finish
            print("step 11")
            self.ego.target_gear = 0
            if self.ego.target_gear == 0:
                self.eleventh_stop = True
                sleep(0.2)

    def diagonal_step12(self):
        if self.eleventh_stop and not self.twelfth_stop: # 
            print("step 11")
            self.global_path.x = self.global_path_storage_x # 다시 원래 경로
            self.global_path.y = self.global_path_storage_y
            self.twelfth_stop = True
            sleep(0.2)

    def diagonal_step13(self):
        if self.twelfth_stop and not self.thirteenth_stop: # 
            print("step 12")
            self.target_control(0, 6)
            self.parking.on='off'        
#####################################################################################################

    def delivery_step1(self):
        if not self.first_stop and 3400 <= self.ego.index: # 임의의 인덱스
            print("step 1")
            self.target_control(200, 0)
            if self.ego.speed<0.5:
                self.first_stop = True
                sleep(0.2)

    def delivery_step2(self):
        if self.first_stop and not self.second_stop: 
            
            print("step 2")
            self.global_path_x_storage = self.global_path.x
            self.global_path_y_storage = self.global_path.y

            # 실제 배달 주행을 위한 코드
            # if self.perception.delivery_flag == 1: # 인지로부터 들어온 표지판 넘버
            #     self.delivery_point = np.array([_,_]) # 임의의 배달좌표 1
            # if self.perception.delivery_flag == 2:
            #     self.delivery_point = np.array([_,_]) # 임의의 배달좌표 2
            # if self.perception.delivery_flag == 3:
            #     self.delivery_point = np.array([_,_]) # 임의의 배달좌표 3

            self.delivery_point = np.array([67.9, 73.2]) # simulation을 위한 임의의 배달좌표
            self.delivery_index = self.nearest_index(self.delivery_point[0], self.delivery_point[1])
            global_vect = np.array([self.global_path.x[self.delivery_index + self.add] - self.global_path.x[self.ego.index], self.global_path.y[self.delivery_index + self.add] - self.global_path.y[self.ego.index]])
            inv_global_vect = np.array([self.global_path.x[self.ego.index] - self.global_path.x[self.delivery_index], self.global_path.y[self.ego.index] - self.global_path.y[self.delivery_index]])
            start_delivery_point = self.delivery_point + inv_global_vect
            end_delivery_point = np.array([start_delivery_point[0] + global_vect[0], start_delivery_point[1] + global_vect[1]])
            delivery_path_x = [start_delivery_point[0], end_delivery_point[0]]
            delivery_path_y = [start_delivery_point[1], end_delivery_point[1]]
            cx, cy, _, _, _ = calc_spline_course(delivery_path_x, delivery_path_y ,ds = 0.1)
            self.global_path.x, self.global_path.y = cx, cy
            self.second_stop = True
            sleep(0.2)

    def delivery_step3(self):
        if self.second_stop and not self.third_stop:
            print("step 3")
            self.target_control(0,3)
            if len(self.global_path.x) - self.add <= self.ego.index :
                self.target_control(200, 0)
                if self.ego.speed<0.5:
                    self.third_stop = True
                    self.global_path.x = self.global_path_x_storage
                    self.global_path.y = self.global_path_y_storage
                    sleep(0.2)

    def delivery_step4(self): # finish
        if self.third_stop and not self.fourth_stop:
            print("step 4")
            self.target_control(0,5)
            self.plan.behavior_decision = "go"
    
##############################################################################################################
    # 객체 생성 및 초기화
    def Potential_field0(self):
        self.k.acquire()
        pf = Potential_field(self.ego)
        local_path = Path()
        local_path.x = []
        local_path.y = []
        vehicle_position = np.array([self.ego.x,self.ego.y])
        
        if len(self.jiamtong)>20:
            self.jiamtong.pop(0)
        
        self.jiamtong.append(vehicle_position)
        ind = self.nearest_index2(self.ego.x,self.ego.y)
        obstacles = self.invisible_wall2[ind-15:ind+15].copy()

        self.tmp_vehicle_position = np.array([vehicle_position[0], vehicle_position[1]]) # [106.4777,127.0755]
        # obstacle = [[104.1116,122.6361],[106.4777,127.0755],[103.668,122.4512],[102.7807,122.6362],[108.1045,126.1506],[107.6608,126.3356]]
        obstacle = [[104.1116,122.6361],[102.7807,122.6362],[107.6608,126.3356]]

        #######실험실#########내적해서 내가 지나간 장애물은 고려안해버리긔 
        tmp1 = np.array([(self.global_path.x[self.ego.index+1]-self.ego.x),
                         (self.global_path.y[self.ego.index+1]-self.ego.y)])
        tmp1 = self.inc/(np.linalg.norm(tmp1))
        for obs in obstacle:
            # tmp2 = np.array([(obs[0]-self.ego.x),
            #                  (obs[1]-self.ego.y)])
            # if np.dot(tmp1,tmp2) >0:
                obstacles.append(obs)
        ##############################################################
        goal_position = np.array([self.global_path.x[self.ego.index+100], self.global_path.y[self.ego.index+100]])

        ####hy_obs### 앞에 장애물 갯수많큼 팔러워 넣기~ 
        if len(self.jiamtong)>5:
            follower = self.jiamtong[-5]
        else:
            follower = self.jiamtong[-1]
        
        for _ in range((len(obstacle)//2)):
            obstacles.append(follower)
    

        #########local_path update !!!#################
        for _ in range(100):
            self.tmp_vehicle_position = self.tmp_vehicle_position + pf.potential
            local_path.x.append(list(self.tmp_vehicle_position)[0])
            local_path.y.append(list(self.tmp_vehicle_position)[1])
            local_path.mission.append("obs_tmp")
            pf.update(self.tmp_vehicle_position, goal_position, obstacles)
            pf.run()
        
        self.local_path.x = local_path.x
        self.local_path.y = local_path.y
        self.shared.hy_test = obstacles
        self.k.release()
    
    def PF_labotary(self): #1457
        obstacles = []
        obstacle = [[104.1116,122.6361],[102.7807,122.6362]]#,[107.6608,126.3356]]
        tmp = np.array([(self.global_path.x[self.ego.index+1]-self.ego.x),   # 내 앞방향 벡터
                         (self.global_path.y[self.ego.index+1]-self.ego.y)])
        if self.ego.index > 1457: #임시로 
                obstacle.append([106.4777,127.0755]) # 
        for obs2 in obstacle: # obstacle은 일단 인지된 장애물이라 가정함 
                tmp0 = np.array([(obs2[0]-self.ego.x),
                             (obs2[1]-self.ego.y)])
                if np.dot(tmp,tmp0) >0:
                        obstacles.append(obs2)     # 내가 장애물 지나면 없애버림 
        # if len(self.ego_trace)>20: 
        #     self.ego_trace.pop(0)
        # self.ego_trace.append(vehicle_position) # for follower 
        self.shared.hy_test = obstacles # obstacle's'임 진짜 장애물 최종_진짜_찐_마지막_찐찐_진짜
        if self.flag: #처음에는 한번 돌려주고 장애물 갯수 저장하기
            self.cal_pf(obstacles)
            self.flag = False
            self.prev = len(obstacles)
        elif self.prev != len(obstacles): # 장애물 갯수가 없어지거나 더하지든 없어지든 다시 계산 
            self.cal_pf(obstacles)
            self.prev = len(obstacles)
        elif self.prev == len(obstacles):
           pass
        else:
            self.local_path.x = self.global_path.x
            self.local_path.y = self.global_path.y
    
    def cal_pf(self,obstacles):    
        self.k.acquire()
        pf = Potential_field(self.ego)
        local_path = Path()
        local_path.x = []
        local_path.y = []
        #
        goal_position = np.array([self.global_path.x[self.ego.index+100], self.global_path.y[self.ego.index+100]])
        #
        local_path.x.append(self.ego.x)
        local_path.y.append(self.ego.y)
        off_set = 2
        for obs in obstacles:
            jiamtong = []
            ind = self.nearest_index(obs[0],obs[1])
            tm = np.array([self.global_path.x[ind],self.global_path.y[ind]])
            tmp1 = tm + self.inv_inc * off_set
            tmp2 = tm - self.inv_inc * off_set
            jiamtong.append(obs)
            jiamtong.append(tmp1)
            jiamtong.append(tmp2)
            pf.update(tm,goal_position,jiamtong)
            pf.run()
            tm = tm + pf.potential
            local_path.x.append(list(tm[0]))
            local_path.y.append(list(tm[1]))
        
        local_path.x.append(self.global_path.x[self.ego.index + 30])
        local_path.y.append(self.global_path.y[self.ego.index + 30])
        local_path.x, local_path.y, _, _,_ = calc_spline_course(local_path.x,local_path.y)
        self.local_path.x = local_path.x
        self.local_path.y = local_path.y
            
    def nearest_index2(self, pointx, pointy):
        dist = []
        dx = []
        dy = []
        for j in range(len(self.invisible_wall2)):
            dx.append((pointx - self.invisible_wall2[j][0]))
            dy.append((pointy - self.invisible_wall2[j][1]))
        for i in range(len(dx)):
            distx = dx[i]
            disty = dy[i]
            dist.append(np.hypot(distx, disty))

        ind = int(np.argmin(dist))
        
        return ind

    def invisible_wall(self):

        # virtual wall
        self.k.acquire()
        space = 0.5
        left_offset = 2
        right_offset = 2
        # first_index = 1235
        first_index = 600
        tm = np.array([self.global_path.x[first_index],self.global_path.y[first_index]])#내 인덱스에서 글로벌 좌표
        self.inc = np.array([(self.global_path.x[first_index+5]-self.global_path.x[first_index]),(self.global_path.y[first_index+5]-self.global_path.y[first_index])])
        self.inc = self.inc/(np.linalg.norm(self.inc))
        self.inv_inc=np.array([-(self.global_path.y[first_index+1]-self.global_path.y[first_index]),(self.global_path.x[first_index+1]-self.global_path.x[first_index])])
        self.inv_inc = self.inv_inc/(np.linalg.norm(self.inv_inc))
        print('inv_inc',self.inv_inc)
        for i in range(200): 
            tmp1= tm + self.inv_inc * left_offset + self.inc * i * space  # [x,y]
            tmp2= tm - self.inv_inc * right_offset + self.inc * i * space
            self.invisible_wall2.append(list(tmp1))
            self.invisible_wall2.append(list(tmp2))
        self.k.release()
