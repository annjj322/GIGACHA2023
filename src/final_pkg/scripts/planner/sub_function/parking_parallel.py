# import pymap3d
# import json
# from shared.path import Path
# from math import cos, degrees, radians, sin, atan2, sqrt, hypot
# from numpy import rad2deg
# import csv
# from .cubic_spline_planner import calc_spline_course
# from shared.path import Path

# class Parking_Motion():
#     def __init__(self, sh, pl, eg):
#         self.shared = sh
#         self.plan = pl
#         self.ego = eg

#         self.global_path = self.shared.global_path
#         self.parking = self.shared.park

#         self.tmp_backward_path = Path()

#         #simul kcity
#         self.base_lat = 37.23873
#         self.base_lon = 126.772383333333
#         self.base_alt = 15.4
#         with open('/home/gigacha/TEAM-GIGACHA/src/final_pkg/scripts/planner/sub_function/parking_JSON/parking_KCity_parallel.json') as pkc:
#             self.parking_point = json.load(pkc)

#         # siheung
#         # self.base_lat = 37.36458356
#         # self.base_lon = 126.7237789
#         # self.base_alt = 15.4
#         # with open('/home/gigacha/TEAM-GIGACHA/src/final_pkg/scripts/planner/sub_function/parking_JSON/parking_Siheung_parallel.json') as pkc:
#         #     self.parking_point = json.load(pkc)

#         self.radius = 1.15
#         # minimun_radius == 1.95
#         self.o1_x = 0.5
#         self.long = 0
#         self.mapname = ''
#         self.cnt = False
#         self.cnt2 = False
        

#     def make_parking_tra(self):
#         # self.point = self.parking_point[str(1)]
#         self.point = self.parking_point[str(self.parking.select_num)]
#         self.start_point = self.point["start"]
#         self.end_point = self.point["end"]
#         if self.cnt2 == False:
#             self.cnt2 = True
#             self.findParkingPath()

#     def findParkingPath(self):

#         self.parking_x, self.parking_y = self.parking_call_back(self.start_point[0],self.start_point[1])
#         self.parking_end_x, self.parking_end_y = self.parking_call_back(self.end_point[0],self.end_point[1])

#         self.parking_width = hypot(self.parking_end_y - self.parking_y, self.parking_end_x - self.parking_x)
#         self.heading = rad2deg(atan2((self.parking_end_y - self.parking_y),(self.parking_end_x - self.parking_x)))%360
#         print(f"self.heading : {self.heading}")

#         self.find_O1()

#         O2_radius = self.find_O2()
 
#         heading_O2_O1 = rad2deg(atan2(self.radius, self.parking_width))


#         ex, ey = self.parking.o2x + (O2_radius) * cos(radians(self.heading + 90)), self.parking.o2y + (O2_radius) * sin(radians(self.heading + 90))
#         sx, sy = ex + self.o1_x*cos(radians(self.heading)), ey + self.o1_x*sin(radians(self.heading)) 
        
#         self.make_straight_path(sx, sy, ex, ey)

#         self.make_path(self.parking.o2x, self.parking.o2y, self.heading + 90, self.heading + 180 - heading_O2_O1 , O2_radius, 1)
#         self.parking.incflection_point = len(self.parking.backward_path.x) - 1
#         print(self.parking.incflection_point)
#         self.make_path(self.parking.o1x, self.parking.o1y, self.heading - heading_O2_O1  , self.heading - 90, self.radius, -1)

#         sx, sy = self.parking_x + self.o1_x*cos(radians(self.heading)), self.parking_y + self.o1_x*sin(radians(self.heading))
#         ex, ey = self.parking_x, self.parking_y
#         self.make_straight_path(sx, sy, ex, ey)  

#         print(len(self.parking.backward_path.x))

#         self.parking.forward_path.x, self.parking.forward_path.y = list(reversed(self.parking.backward_path.x)), list(reversed(self.parking.backward_path.y))  

#         min_index = 0
#         min_dis = 10000000
        
#         ######### 주차점과 가장 가까운 path 점 찾기 ########
#         for i in range(len(self.global_path.x)):
#             dx = self.parking_end_x - self.global_path.x[i]
#             dy = self.parking_end_y - self.global_path.y[i]
#             dis = sqrt(dx*dx + dy*dy)
#             if dis < min_dis:
#                 min_dis = dis
#                 min_index = i

#         self.parking.mindex = min_index + (self.o1_x + self.long)*10

#     def parking_call_back(self,x1,y1):
#         x, y, _ = pymap3d.geodetic2enu(x1, y1, self.base_alt,
#                                     self.base_lat, self.base_lon, self.base_alt)
#         return x, y

#     def find_O1(self):
#         dis_P1_O1 = hypot(self.radius, self.o1_x)
#         heading_P1_O1 = rad2deg(atan2(self.o1_x, self.radius))
#         heading_O1 = (self.heading + 90 - heading_P1_O1)
#         self.parking.o1x = self.parking_x + dis_P1_O1 * cos(radians(heading_O1))
#         self.parking.o1y = self.parking_y + dis_P1_O1 * sin(radians(heading_O1))

#     def find_O2(self):
#         def func(a,b,c):
#             print("1 : ", (-b+sqrt(b**2-4*a*c))/2*a)
#             print("2 : ", (-b-sqrt(b**2-4*a*c))/2*a)
#             return max((-b+sqrt(b**2-4*a*c))/2*a, (-b-sqrt(b**2-4*a*c))/2*a)

#         O2_radius = func(1,2*self.radius,-self.parking_width**2)

#         self.parking.o2x = self.parking_end_x + self.o1_x*cos(radians(self.heading))
#         self.parking.o2y = self.parking_end_y + self.o1_x*sin(radians(self.heading))

#         return O2_radius

#     def make_path(self, x, y, start, end, radius, direction):
#         self.tmp_backward_path.x = []
#         self.tmp_backward_path.y = []
#         middle = (start+end)/2

#         self.tmp_backward_path.x.append(x+radius*cos(radians(start)))
#         self.tmp_backward_path.y.append(y+radius*sin(radians(start)))
#         self.tmp_backward_path.x.append(x+radius*cos(radians(middle)))
#         self.tmp_backward_path.y.append(y+radius*sin(radians(middle)))
#         self.tmp_backward_path.x.append(x+radius*cos(radians(end)))
#         self.tmp_backward_path.y.append(y+radius*sin(radians(end)))

#         self.make_curve_path(self.tmp_backward_path)


#     def make_curve_path(self,path):
#         cx, cy, _, _, _ = calc_spline_course(path.x, path.y ,ds = 0.1)

#         self.parking.backward_path.x.extend(cx)
#         self.parking.backward_path.y.extend(cy)

#     def make_straight_path(self, sx, sy, ex, ey):
        
#         x = []
#         y = []
        
#         x.append(sx)
#         x.append(ex)
#         y.append(sy)
#         y.append(ey)
        
#         print(x, y)
#         cx, cy, _, _, _ = calc_spline_course(x, y ,ds = 0.1)
         
#         self.parking.backward_path.x.extend(cx)
#         self.parking.backward_path.y.extend(cy)

#     def park_index_finder(self,path):
#         min_dis = -1
#         min_idx = 0
#         step_size = 10
#         save_idx = self.parking.index

#         for i in range(max(self.parking.index - step_size, 0), self.parking.index + step_size):
#             try:
#                 dis = hypot(
#                     path.x[i] - self.ego.x, path.y[i] - self.ego.y)
#             except IndexError:
#                 break
#             if (min_dis > dis or min_dis == -1) and save_idx <= i:
#                 min_dis = dis
#                 min_idx = i
#                 save_idx = i

#         return min_idx

#     def parking_drive(self, direction):
#         self.parking.direction = direction

#         if self.parking.direction == 0:
#             if self.cnt == False:
#                 self.parking.index = 0
#                 self.cnt = True
#             path = self.parking.forward_path
#         else:
#             path = self.parking.backward_path

#         self.parking.index = self.park_index_finder(path)
#         self.parking.stop_index = len(path.x)