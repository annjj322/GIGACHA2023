import pymap3d
import json
from shared.path import Path
from math import cos, degrees, radians, sin, atan2, sqrt, hypot
from numpy import rad2deg
import csv
from .cubic_spline_planner import calc_spline_course

class Parking_Motion():
    def __init__(self, sh, pl, eg):
        self.shared = sh
        self.plan = pl
        self.ego = eg

        self.global_path = self.shared.global_path
        self.parking = self.shared.park

        # simul kcity
        self.base_lat = 37.23873
        self.base_lon = 126.772383333333
        self.base_alt = 15.4
        with open('/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/planner/sub_function/parking_JSON/parking_KCity.json') as pkc:
            self.parking_point = json.load(pkc)
        self.direction = -1

        # #siheung
        # self.base_lat = 37.36458356
        # self.base_lon = 126.7237789
        # self.base_alt = 15.4
        # with open('/home/gigacha/TEAM-GIGACHA/src/final_pkg/scripts/planner/sub_function/parking_JSON/parking_siheung.json') as pkc:
        #     self.parking_point = json.load(pkc)
        # self.direction = 1

        self.tmp_forward_path = Path()
        self.list_radius = [7, 9, 7, 8, 7, 8]
        self.smooth_radius = 0
        self.cnt = False

    def make_parking_tra(self):
        self.point = self.parking_point[str(self.parking.select_num)]
        self.smooth_radius = self.list_radius[int(self.parking.select_num) - 1]
        self.start_point = self.point["start"]
        self.end_point = self.point["end"]
        if len(self.parking.forward_path.x) == 0:
            self.findParkingPath()

    def findParkingPath(self):
        min_index = 0
        min_dis = 10000000

        self.parking_x, self.parking_y = self.parking_call_back(self.start_point[0],self.start_point[1])
        self.parking_end_x, self.parking_end_y = self.parking_call_back(self.end_point[0],self.end_point[1])

        ######### 주차점과 가장 가까운 path 점 찾기 ########
        for i in range(len(self.global_path.x)):
            dx = self.parking_x - self.global_path.x[i]
            dy = self.parking_y - self.global_path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis:
                min_dis = dis
                min_index = i

        self.parking.mindex = min_index

        self.heading = rad2deg(atan2(
            (self.global_path.y[self.parking.mindex]-self.global_path.y[self.parking.mindex - 1]), (self.global_path.x[self.parking.mindex]-self.global_path.x[self.parking.mindex - 1])))%360

        print(f"self.heading : {self.heading}")

        theta_O3_to_lot = self.find_O3()
        self.make_path(self.parking.o3x, self.parking.o3y, self.heading - self.direction*90, self.heading - self.direction*90 + self.direction*theta_O3_to_lot, self.smooth_radius, self.direction*1)

        self.parking.backward_path.x, self.parking.backward_path.y = list(reversed(self.parking.forward_path.x)), list(reversed(self.parking.forward_path.y))  

    
    def parking_call_back(self,x1,y1):
        x, y, _ = pymap3d.geodetic2enu(x1, y1, self.base_alt,
                                    self.base_lat, self.base_lon, self.base_alt)
        return x, y


    def find_O3(self):

        dis_mindex_to_lot = sqrt((self.parking_x - self.global_path.x[self.parking.mindex])**2 + (
            self.parking_y - self.global_path.y[self.parking.mindex])**2)
        dis_mindex_to_start = sqrt(2*dis_mindex_to_lot *
                                self.smooth_radius - dis_mindex_to_lot**2)

        self.start_index = self.parking.mindex - round(10*dis_mindex_to_start)

        # self.park_heading = rad2deg(atan2(
        #     (self.parking_end_y-self.parking_y), (self.parking_end_x-self.parking_x)))%360

        # self.park_heading = (self.park_heading - 90)%360

        theta_O3_to_lot = rad2deg(
            atan2(dis_mindex_to_start/(self.smooth_radius-dis_mindex_to_lot), 1))
        # self.park_heading = -1*(90 - theta_O3_to_lot)
        self.parking.o3x = self.global_path.x[self.start_index] + self.smooth_radius*cos(radians((self.heading -90)%360))
        self.parking.o3y = self.global_path.y[self.start_index] + self.smooth_radius*sin(radians((self.heading -90)%360))

        # self.parking.o3x = self.parking_x + self.smooth_radius*cos(radians(self.park_heading)) - self.smooth_radius*sin(radians(self.park_heading))
        # self.parking.o3y = self.parking_y + self.smooth_radius*sin(radians(self.park_heading)) + self.smooth_radius*cos(radians(self.park_heading))
        
        return  theta_O3_to_lot
    # def find_O3(self):

    #         dis_mindex_to_lot = sqrt((self.parking_x - self.global_path.x[self.parking.mindex])**2 + (
    #             self.parking_y - self.global_path.y[self.parking.mindex])**2)
    #         dis_mindex_to_start = sqrt(2*dis_mindex_to_lot *
    #                                 self.smooth_radius - dis_mindex_to_lot**2)

    #         vvv = (self.parking_y - self.parking_end_y)/(self.parking_end_x - self.parking_x)

    #         self.parking.o3y = sqrt((self.smooth_radius**2)/((vvv)**2+1)) + self.parking_y

    #         self.parking.o3x = (self.parking.o3y - self.parking_y)*(vvv) + self.parking_x

    #         theta_O3_to_lot = rad2deg(
    #             atan2(dis_mindex_to_start/(self.smooth_radius-dis_mindex_to_lot), 1))
    #         # self.parking.o3x = self.parking_x + self.smooth_radius*cos(radians(self.park_heading)) - self.smooth_radius*sin(radians(self.park_heading))
    #         # self.parking.o3y = self.parking_y + self.smooth_radius*sin(radians(self.park_heading)) + self.smooth_radius*cos(radians(self.park_heading))
            
    #         return  theta_O3_to_lot                  
    
    def make_path(self, x, y, start, end, radius, direction):
        start = int(round(start))
        end = int(round(end))

        # for i in range(0,30):
        #     self.parking.forward_path.x.append(self.global_path.x[self.start_index -30 +i])
        #     self.parking.forward_path.y.append(self.global_path.y[self.start_index -30 +i])

        for theta in range(start, end, direction):
            self.tmp_forward_path.x.append(x+radius*cos(radians(theta)))
            self.tmp_forward_path.y.append(y+radius*sin(radians(theta)))

        self.make_curve_path()
        self.make_straight_path()

    def make_curve_path(self):
        middle_index = int(len(self.tmp_forward_path.x) / 2)
        sx, sy = self.tmp_forward_path.x[0], self.tmp_forward_path.y[0]
        mx, my = self.tmp_forward_path.x[middle_index], self.tmp_forward_path.y[middle_index]
        ex, ey = self.parking_x, self.parking_y
        
        x = []
        y = []
        
        x.append(sx)
        x.append(mx)
        x.append(ex)
        y.append(sy)
        y.append(my)
        y.append(ey)
        
        cx, cy, _, _, _ = calc_spline_course(x, y ,ds = 0.1)
         
        self.parking.forward_path.x.extend(cx)
        self.parking.forward_path.y.extend(cy)

    def make_straight_path(self):
        sx,sy,ex,ey = self.parking_x, self.parking_y, self.parking_end_x, self.parking_end_y
        
        x = []
        y = []
        
        x.append(sx)
        x.append(ex)
        y.append(sy)
        y.append(ey)
        
        cx, cy, _, _, _ = calc_spline_course(x, y ,ds = 0.1)
         
        self.parking.forward_path.x.extend(cx)
        self.parking.forward_path.y.extend(cy)

    def park_index_finder(self,path):
        min_dis = -1
        min_idx = 0
        step_size = 10
        save_idx = self.parking.index

        for i in range(max(self.parking.index - step_size, 0), self.parking.index + step_size):
            try:
                dis = hypot(
                    path.x[i] - self.ego.x, path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i

        return min_idx

    def parking_drive(self, direction):
        self.parking.direction = direction

        if self.parking.direction == 2:
            if self.cnt == False:
                self.parking.index = 0
                self.cnt = True
            path = self.parking.backward_path
        else:
            path = self.parking.forward_path

        self.parking.index = self.park_index_finder(path)
        self.parking.stop_index = len(path.x)
        # print(self.parking.stop_index)