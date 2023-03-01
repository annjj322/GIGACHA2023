class LonController():
    def __init__(self, eg, sh):
        self.ego = eg
        self.shared = sh

    def run(self): 
        return self.ego.target_speed

# import threading
# import numpy as np
# import rospy
# from local_pkg.msg import Control_Info
# from time import sleep
# from math import hypot, cos, sin, degrees, atan2, radians, pi,sqrt

# class LonController(threading.Thread):
#     def __init__(self, parent, rate):
#         super().__init__()
#         self.period = 1.0 / rate
#         self.shared = parent.shared
#         self.ego = parent.shared.ego
#         self.plan = parent.shared.plan

#         self.lattice_path = parent.shared.lattice_path

#         self.car_max_speed = 10
#         self.road_friction = 0.15

#         self.serial_pub = rospy.Publisher("controller", Control_Info, queue_size=1)

#     def curve_based_velocity(self, path, point_num):

#         out_vel_plan = []

#         for i in range(0,point_num):
#             out_vel_plan.append(self.car_max_speed)
#         print("len : ",len(path.x))
#         for i in range(point_num,len(path.x) - point_num):
        
#             x_list = []
#             y_list = []
#             for box in  range(-point_num, point_num):
#                 x = path.x[i+box]
#                 y = path.y[i+box]
#                 x_list.append([-2*x,-2*y,1])
#                 y_list.append(-(x*x)-(y*y))
                
#             x_matrix = np.array(x_list)
#             y_matrix = np.array(y_list)
#             x_trans = x_matrix.T
                
#             a_matrix = np.linalg.inv(x_trans.dot(x_matrix)).dot(x_trans).dot(y_matrix)
#             a = a_matrix[0]
#             b = a_matrix[1]
#             c = a_matrix[2]
#             r = sqrt(a*a+b*b-c)
#             v_max = sqrt(r*9.8*self.road_friction)  # 0.7
#             if v_max > self.car_max_speed :
#                 v_max = self.car_max_speed
#             out_vel_plan.append(v_max)
#         for i in range(len(path.x)-point_num,len(path.x)):
#             out_vel_plan.append(self.car_max_speed)
            
#         return out_vel_plan


#     def run(self): 
#         while True:
#             try:
#                 # path = self.lattice_path[self.shared.selected_lane]
#                 # self.speed = self.curve_based_velocity(path,20)
                
#                 # self.speed = self.velocity_based_curve(path, 30)
#                 # self.ego.input_speed = self.speed[0]
                
#                 self.ego.input_estop = self.ego.target_estop
#                 self.ego.input_speed = self.ego.target_speed
#                 self.ego.input_gear = self.ego.target_gear
#                 self.ego.input_brake = self.ego.target_brake
#                 if self.ego.target_estop == 0:
#                     self.ego.input_estop = 0x00
#                 elif self.ego.target_estop == 1:
#                     self.ego.input_estop = 0x01

#                 ######################## SERIAL ################################
#                 serial = Control_Info()
#                 serial.emergency_stop = self.ego.input_estop
#                 serial.gear = self.ego.input_gear
#                 serial.speed = self.ego.input_speed
#                 serial.steer = self.ego.input_steer
#                 serial.brake = self.ego.input_brake

#                 self.serial_pub.publish(serial)

#             except IndexError:
#                 print("++++++++lon_controller+++++++++")

#             sleep(self.period)