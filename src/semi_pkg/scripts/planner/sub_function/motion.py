from time import sleep
import numpy as np
from shared.path import Path
from .cubic_spline_planner import calc_spline_course
from math import hypot,atan2,sin,cos,pi,sqrt,radians
import threading
# import rospy
# from nav_msgs.msg import Path as Path2
import threading
import rospy
from visualization_msgs.msg import MarkerArray, Marker

class Potential_field():
    def __init__(self, ego):
        self.repulsive = np.array([0, 0])
        self.attractive = np.array([0, 0])
        self.potential = np.array([0, 0])

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

            

            # print("repulsive unit vec:", unit_vector)
            repulsive += unit_vector * scale
            repulsive_scale += scale
            # print("repulsive", repulsive)
        return repulsive, repulsive_scale
    
    def calculate_attractive_field(self):
        distance = np.linalg.norm(self.vehicle_position - self.goal_position)
        distance += 0.01
        ###
        scale = 30
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
        self.potential_scale = 0.1
        self.potential = self.potential*self.potential_scale

     

    def run(self):
        self.pf_lock.acquire()
        repulsive, rep_scale = self.calculate_repulsive_field()
        attractive, att_scale = self.calculate_attractive_field()
        self.calculate_potential_field(repulsive, rep_scale, attractive, att_scale)
        self.pf_lock.release()

    

class Motion():
    def __init__(self, sh, pl, eg, pk):
        self.pub = rospy.Publisher("/points_hy", MarkerArray, queue_size=1)
        self.msg = Marker()
        self.marker_array = MarkerArray()
        
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

        # diagonal parking
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

        self.global_path_x_storage = []
        self.global_path_y_storage = []
        

        # potential field
        self.potential_lock = threading.Lock()
        self.obstacles = []
        self.local_path = self.shared.local_path
        self.obstacles = self.shared.obstacles
        
        # obstacle avoidance
        self.invisible_wall=[]
        self.tmp_vehicle_position = None
        self.create_invisible_wall()
        self.trace = []
        self.prev = 0
        self.flag = None
        # self.obstacle_map_x = self.global_path.x[1259:1684]
        # self.obstacle_map_y = self.global_path.y[1259:1684]
        self.obstacle_map_x = self.global_path.x[1200:1700]
        self.obstacle_map_y = self.global_path.y[1200:1700]

    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed
    
    def nearest_index(self, pointx, pointy):
        dist = []
        dx = [pointx - x for x in self.global_path.x[0:-1]]
        dy = [pointy - y for y in self.global_path.y[0:-1]]
        for i in range(len(dx)):
            dist.append(np.hypot(dx[i], dy[i]))

        ind = int(np.argmin(dist))
        
        return ind

    def go(self):
        pass

################# PARRALLEL PARKING ###################################################

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

################# DIAGONAL PARKING ###################################################

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

################# DELIVERY ###################################################

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
    
################# STATIC OBSTACLE AVOIDANCE ##################################
    
    def potential_field(self):#
        self.potential_lock.acquire()
        pf = Potential_field(self.ego)
        local_path = Path()
        local_path.x = []
        local_path.y = []
        vehicle_position = np.array([self.ego.x,self.ego.y])
        
        if len(self.trace)>20:
            self.trace.pop(0)
        
        self.trace.append(vehicle_position)
        ind = self.find_wall_index(self.ego.x,self.ego.y)
        obstacles = self.invisible_wall[ind-15:ind+15].copy()

        # obstacle = [[104.1116,122.6361],[106.4777,127.0755],[103.668,122.4512],[102.7807,122.6362],[108.1045,126.1506],[107.6608,126.3356]]
        obstacle = [[104.1116,122.6361],[102.7807,122.6362],[107.6608,126.3356]]

        for obs in obstacle:
                obstacles.append(obs)

        goal_position = np.array([self.global_path.x[self.ego.index+50], self.global_path.y[self.ego.index+50]])


        # if len(self.trace)>10:
        #     follower = self.trace[-1]
        # else:
        #     follower = self.trace[-1]
        follower = self.trace[0]
        
        for _ in range((len(obstacle)//2)):
            obstacles.append(follower)
    

        #########local_path update !!!#################
        self.jmtmp = -np.array(self.jmtmp)
        for _ in range(30):
            # print(self.jmtmp)
            # print(pf.potential)
            # print()
            # print(np.dot(self.jmtmp, pf.potential))
            if np.dot(self.jmtmp, pf.potential) > 0:
                tmp1 = np.array([self.jmtmp[0], self.jmtmp[1], 0])
                tmp2 = np.array([pf.potential[0], pf.potential[1], 0])
                if np.cross(tmp1, tmp2)[2] < 0:
                    pf.potential = -self.jmtmp2*pf.potential_scale
                else:
                    pf.potential = self.jmtmp2*pf.potential_scale
                    
            vehicle_position = vehicle_position + pf.potential
            
            local_path.x.append(list(vehicle_position)[0])
            local_path.y.append(list(vehicle_position)[1])
            local_path.mission.append("obs_tmp")
            pf.update(vehicle_position, goal_position, obstacles)
            pf.run()
        
        self.local_path.x = local_path.x
        self.local_path.y = local_path.y
        self.shared.obstacles = obstacles

        self.potential_lock.release()
    
    def find_wall_index(self, pointx, pointy):#가상벽에서 인덱스계산기 
        dist = []
        dx = []
        dy = []
        for j in range(len(self.invisible_wall)):
            dx.append((pointx - self.invisible_wall[j][0]))
            dy.append((pointy - self.invisible_wall[j][1]))
        for i in range(len(dx)):
            distx = dx[i]
            disty = dy[i]
            dist.append(np.hypot(distx, disty))

        ind = int(np.argmin(dist))
        
        return ind

    def create_invisible_wall(self):#가상벽 생성기
        self.potential_lock.acquire()

        # wall parameters
        space = 1
        left_offset = 3
        right_offset = 3


        first_index = 600
        start_point = np.array([self.global_path.x[first_index],self.global_path.y[first_index]])#내 인덱스에서 글로벌 좌표

        global_path_incline = np.array([(self.global_path.x[first_index+5]-self.global_path.x[first_index]),(self.global_path.y[first_index+5]-self.global_path.y[first_index])])
        global_path_incline = global_path_incline/(np.linalg.norm(global_path_incline))
        self.jmtmp = global_path_incline

        inv_inc = np.array([-(self.global_path.y[first_index+1]-self.global_path.y[first_index]),(self.global_path.x[first_index+1]-self.global_path.x[first_index])])
        inv_inc = inv_inc/(np.linalg.norm(inv_inc))
        self.jmtmp2 = inv_inc

        for i in range(200): 
            left_wall = start_point + inv_inc * left_offset + global_path_incline * i * space  # [x,y]
            right_wall = start_point - inv_inc * right_offset + global_path_incline * i * space
            self.invisible_wall.append(list(left_wall))
            self.invisible_wall.append(list(right_wall))

        self.potential_lock.release()

    def nearest_index2(self, pointx, pointy):
        dist = []
        dx = [pointx - x for x in self.obstacle_map_x[0:-1]]
        dy = [pointy - y for y in self.obstacle_map_y[0:-1]]
        for i in range(len(dx)):
            dist.append(np.hypot(dx[i], dy[i]))

        ind = int(np.argmin(dist))
        
        return ind
 
    def get_three_points(self, middle_point, width, length):#점과 가로 세로로 장애물 세점 얻어내기
        #TODO(1) : make four points
        r = sqrt(width**2 + length**2)/2
        alpha = atan2(width, length)
        theta = radians(self.ego.heading)
        p1 = [middle_point[0] + r*cos(alpha+theta), middle_point[1] + r*sin(alpha+theta)]
        p2 = [middle_point[0] + r*cos(alpha-theta+pi), middle_point[1] + r*sin(alpha-theta+pi)]
        p3 = [middle_point[0] + r*cos(alpha+theta+pi), middle_point[1] + r*sin(alpha+theta+pi)]
        p4 = [middle_point[0] + r*cos(alpha-theta), middle_point[1] + r*sin(alpha-theta)]
        points = [p1, p2, p3, p4]
        self.marker_array = MarkerArray()
        
        for ind, point in enumerate(points):
            msg = Marker()  # Create a new Marker message for each point
            
            msg.header.frame_id = "map"
            msg.pose.position.x = point[0]
            msg.pose.position.y = point[1]
            msg.pose.position.z = 0.0
            msg.pose.orientation.w = 1.0  # Identity orientation
            
            msg.id = ind  # Use the index as the ID for uniqueness
            msg.type = Marker.SPHERE
            msg.action = Marker.ADD
            msg.color.a = 1.0  # Fully opaque color
            msg.color.r = 1.0  # Red color
            msg.color.g = 0.0
            msg.color.b = 0.0
            
            msg.scale.x = 0.1
            msg.scale.y = 0.1
            msg.scale.z = 0.1
            
            msg.frame_locked = True
            self.marker_array.markers.append(msg)
        self.pub.publish(self.marker_array)


        #1259~1684
        ##################검증 완

        point_idxs_N_distance = []
        for point in points:
           point_idx = self.nearest_index2(point[0], point[1])
           distance = self.distance_points(point, [self.obstacle_map_x[point_idx], self.obstacle_map_y[point_idx]])
           point_idxs_N_distance.append([point[0], point[1], point_idx, distance]) # 각 point에 대한 [x, y, index, distance]
        

        #TODO(2) : sort by index
        point_idxs_N_distance.sort(key=lambda x: x[2])

        for point in point_idxs_N_distance:
            print(point[2])

        #TODO(3) : delete the most distant point
        max_value = max(point_idxs_N_distance, key=lambda x: x[3])
        extracted_point_idxs_N_distance = [element for element in point_idxs_N_distance if element != max_value]

        return extracted_point_idxs_N_distance
    
    def distance_points(self, point1, point2):#두 점 사이 거리 계산기
        dx = point1[0]-point2[0]
        dy = point1[1]-point2[1]
        return hypot(dx, dy)
    
    def left_or_right(self, middle_point):#왼쪽, 오른쪽 판단기
        obs_idx = self.nearest_index2(middle_point[0], middle_point[1])
        global_path_vector = np.array([self.obstacle_map_x[obs_idx+3]-self.obstacle_map_x[obs_idx],
                                       self.obstacle_map_y[obs_idx+3]-self.obstacle_map_y[obs_idx], 
                                       0                                                        ])
        obs_from_path_vector = np.array([middle_point[0]-self.obstacle_map_x[obs_idx], 
                                         middle_point[1]-self.obstacle_map_y[obs_idx], 
                                         0                                          ])

        if np.cross(global_path_vector, obs_from_path_vector)[2]>=0:
            print("obstacle is on left")
            return "left"
        else:
            print("obstacle is on right")
            return "right"

    def rotate_vector(self, original_vector, angle):#회전 행렬 적용
        rotation_matrix = np.array([
            [cos(angle), sin(angle)],
            [-sin(angle), cos(angle)]
        ])
        rotated_vector = np.dot(rotation_matrix, original_vector)
        return rotated_vector

    def find_target_points(self, direction, extracted_point_idxs_N_distance): #
        offset = 4
        if direction == "left":
            angle = pi/2
        if direction == "right":
            angle = -pi/2

        middle_points = []
        indices = []
        for point in extracted_point_idxs_N_distance:
            global_path_vector = np.array([
                self.obstacle_map_x[point[2]+3]-self.obstacle_map_x[point[2]],
                self.obstacle_map_y[point[2]+3]-self.obstacle_map_y[point[2]]])
            global_path_unit_vector = global_path_vector/np.linalg.norm(global_path_vector)
            wall_point = np.array([self.obstacle_map_x[point[2]],self.obstacle_map_y[point[2]]]) + self.rotate_vector(global_path_unit_vector, angle) * offset
            
            middle_point = [(point[0]+wall_point[0])/2, (point[1]+wall_point[1])/2] 
            middle_points.append(middle_point)

            indices.append(point[2])

        return middle_points, indices[0], indices[-1] # 시작점+얘+끝점 해서 큐빅돌리기.
    
    def make_path(self, middle_points, start_ind, final_ind) :
        start_offset = - 30
        final_offset = 10
        tmp_x = []
        tmp_y = []
        tmp_x.append(self.obstacle_map_x[start_ind + start_offset - 3])
        tmp_y.append(self.obstacle_map_y[start_ind + start_offset - 3])
        for point in middle_points: 
            tmp_x.append(point[0])
            tmp_y.append(point[1])
        tmp_x.append(self.obstacle_map_x[final_ind + final_offset + 3])
        tmp_y.append(self.obstacle_map_y[final_ind + final_offset + 3])
        tmp_x, tmp_y ,_,_,_ = calc_spline_course(tmp_x, tmp_y)
        self.global_path.x = self.obstacle_map_x[:start_ind + start_offset - 4] + tmp_x + self.obstacle_map_x[final_ind + final_offset + 4:]
        self.global_path.y = self.obstacle_map_y[:start_ind + start_offset - 4] + tmp_y + self.obstacle_map_y[final_ind + final_offset + 4 :]
        tmp = []
        for i in range(len(self.global_path.x)):
            tmp.append('obs_tmp')
        self.global_path.mission =tmp

   
        
    