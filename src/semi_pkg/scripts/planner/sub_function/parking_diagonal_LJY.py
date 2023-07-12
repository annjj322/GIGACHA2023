import pymap3d
import json
from shared.path import Path
from math import cos, degrees, radians, sin, atan2, sqrt, hypot
from numpy import rad2deg, argmin, hypot
import csv
from .cubic_spline_planner import calc_spline_course

class Parking_Motion_LJY():
    def __init__(self, sh, pl, eg):
        self.shared = sh
        self.plan = pl
        self.ego = eg

        self.global_path = self.shared.global_path
        self.parking = self.shared.park

        self.L = 1.04
        self.R = self.L/sin(radians(27))
        self.d = sqrt((self.ego[0] - self.middlepoint[0])**2 + (self.ego[1] - self.middlepoint[1])**2)

##########################################################
        self.path_storage_x = []
        self.path_storage_y = []
##########################################################
        self.Ledgedata = [69.95, 52.16]
        self.Redgedata = [70.98, 54.38]
        self.middlepoint = [(self.Ledgedata[0] + self.Redgedata[0])/2,(self.Ledgedata[1] + self.Redgedata[1])/2]
        dest_x, dest_y = self.find_destination()
        self.destination = [dest_x, dest_y]

    def find_contact(self):
        # find global line
        xs = self.global_path.x[self.shared.ego.index - 10]
        ys = self.global_path.y[self.shared.ego.index - 10]
        xf = self.global_path.x[self.shared.ego.index + 10]
        yf = self.global_path.y[self.shared.ego.index + 10]
        global_inclination = (ys - yf)/(xs - xf)
        global_intercept = -global_inclination*xs + ys

        # find vertical line
        pl_inclination = (self.Ledgedata[1] - self.Redgedata[1])/(self.Ledgedata[0] - self.Redgedata[0])
        vertical_inclination = -1/pl_inclination
        vertical_intercept = -vertical_inclination*self.middlepoint[0] + self.middlepoint[1]

        # find contact point
        cont_x = (global_intercept - vertical_intercept)/(vertical_inclination - global_inclination)
        cont_y = vertical_inclination*cont_x + vertical_intercept

        return cont_x, cont_y
    
    def find_destination(self):
        pl_inclination = (self.Ledgedata[1] - self.Redgedata[1])/(self.Ledgedata[0] - self.Redgedata[0])
        vertical_inclination = -1/pl_inclination
        vertical_inclination_angle = degrees(atan2(vertical_inclination,1))

        if vertical_inclination_angle < 0:
            vertical_inclination_angle += 180
            vertical_inclination_angle %= 360

        dest_x = self.middlepoint[0] + 2.6/(sqrt(vertical_inclination**2+1))
        dest_y = self.middlepoint[1] + 2.6*vertical_inclination/(sqrt(vertical_inclination**2+1))

        return dest_x, dest_y
    
    def nearest_index(self, pointx, pointy):
        dx = [pointx - x for x in self.global_path.x[0:-1]]
        dy = [pointy - y for y in self.global_path.y[0:-1]]
        dist = hypot(dx, dy)

        ind = int(argmin(dist))
        
        return ind

    def making_forward_path(self):
        # ind1 = self.nearest_index(self.ego.x, self.ego.y)
        # cont_x, cont_y = self.find_contact()
        # ind2 = self.nearest_index(cont_x, cont_y)
        
        # print("ind1: ", ind1)
        # print("ind2: ", ind2)

        # parking_sub_x = [self.middlepoint[0], self.destination[0]]
        # parking_sub_y = [self.middlepoint[1], self.destination[1]]

        # sx, sy, syaw, sk, ss = calc_spline_course(parking_sub_x, parking_sub_y, ds = 0.01)

        # if ind1 < ind2-21:
        #     parking_path_x = [self.global_path.x[ind1], self.global_path.x[ind1+1], self.global_path.x[ind2-41], \
        #                 self.global_path.x[ind2-40], self.middlepoint[0], sx[1], sx[-2], sx[-1]]
        #     parking_path_y = [self.global_path.y[ind1], self.global_path.y[ind1+1], self.global_path.y[ind2-41], \
        #                 self.global_path.y[ind2-40], self.middlepoint[1], sy[1], sy[-2], sy[-1]]
        # else:
        #     parking_path_x = [self.global_path.x[ind1], self.global_path.x[ind1+1], \
        #                 self.middlepoint[0], sx[1], sx[-2], sx[-1]]
        #     parking_path_y = [self.global_path.y[ind1], self.global_path.y[ind1+1], \
        #                 self.middlepoint[1], sy[1], sy[-2], sy[-1]]

        # cx, cy, cyaw, ck, s = calc_spline_course(parking_path_x, parking_path_y, ds = 0.01)

        # self.path_storage_x, self.path_storage_y = cx, cy

        # self.global_path.x, self.global_path.y = cx, cy

          
        # ind1 = self.nearest_index(self.ego.x, self.ego.y)

        if self.d < self.R*(1-cos(self.find_inclination(self.Ledgedata, self.Redgedata))):
            vectO_size = abs(sqrt((self.Redgedata[0]-self.Ledgedata[0])**2 + (self.Redgedata[1]-self.Ledgedata[1])**2))
            vectO = [(self.Redgedata[0]-self.Ledgedata[0])/vectO_size, (self.Redgedata[1]-self.Ledgedata[1])/vectO_size] # 단위 벡터
            pO = [self.middlepoint[0]+self.R*vectO[0], self.middlepoint[1]+self.R*vectO[1]]

            xs = self.global_path.x[self.shared.ego.index - 10]
            ys = self.global_path.y[self.shared.ego.index - 10]
            xf = self.global_path.x[self.shared.ego.index + 10]
            yf = self.global_path.y[self.shared.ego.index + 10]
            a1 = (ys - yf)/(xs - xf)
            b1 = -a1*xs + ys

            # find vertical line
            a2 = -1/a1
            b2 = -a2*pO[0] + pO[1]

            # find contact point
            cont_x = (b2 - b1)/(a1 - a2)
            cont_y = a1*cont_x + b1

            # find vector
            vect1_size = abs(sqrt((cont_x - pO[0])**2 + (cont_y - pO[1])**2))
            vect1 = [(cont_x - pO[0])/vect1_size, (cont_y - pO[1])/vect1_size] # 단위 벡터
            
            start_point = [pO[0]+self.R*vectO[0], pO[1]+self.R*vectO[1]]
            

    def find_inclination(self, p1, p2):

        inclination = (p1[1] - p2[1])/(p1[0] - p2[0])

        inclination_angle = degrees(atan2(inclination,1))

        if inclination_angle < 0:
            inclination_angle += 180
            inclination_angle %= 360

        return inclination_angle

        

    def making_reverse_forward_path(self):
        self.global_path.x, self.global_path.y = list(reversed(self.path_storage_x)), list(reversed(self.path_storage_y))  

    def making_backward_path(self):
        ind1 = self.nearest_index(self.ego.x, self.ego.y)
        cont_x, cont_y = self.find_contact()
        ind2 = self.nearest_index(cont_x, cont_y)

        backward_path_x = [self.global_path.x[ind1], self.global_path.x[ind2 - 200]]
        backward_path_y = [self.global_path.y[ind1], self.global_path.y[ind2 - 200]]
        
        cx, cy, cyaw, ck, s = calc_spline_course(backward_path_x, backward_path_y, ds = 0.1)
        
        print("ind1: ",ind1)
        print("ind2: ",ind2)

        self.global_path.x, self.global_path.y = cx, cy  
        
##########################################################

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

        # print(f"self.heading : {self.heading}")

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
        self.parking.stop_index = len(self.global_path.x)