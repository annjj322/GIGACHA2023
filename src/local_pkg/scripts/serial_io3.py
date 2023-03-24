#!/usr/bin/env python3
from sig_int_handler import Activate_Signal_Interrupt_Handler
import serial
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from local_pkg.msg import Local
import threading
import struct
import rospy
from math import sqrt, atan2, sin, atan, cos, sqrt
from numpy import degrees, radians, hypot, array, argmin, arange
import json
import matplotlib.pyplot as plt
from geometry_msgs.msg import PoseArray
import numpy as np
import time


class Serial_IO:
    def __init__(self):
        # self.k = 0.55
        self.k = 0.15
        self.WB = 1.04 # wheel base

        # calculate Error // just for curve path
        self.local4error_pre_x = None
        self.local4error_pre_y = None
        self.local4error_x = None
        self.local4error_y = None
        self.error_dist = 0 # curve index : 3000 ~ 3500
        self.ego_index_pre = None

        # Global Path
        self.global_path_x = []
        self.global_path_y = []

        # Ego information      
        self.curPosition_x = []
        self.curPosition_y = []
        self.velocity = []
        self.ego_speed = []
        self.gps_to_Lidar = 1.3

        # Obstacle information
        self.obj_x = None
        self.obj_y = None
        self.objPosition_x = []
        self.objPosition_y = []

        self.stop_index = [800, 1200, 2500, 4450]
        # self.stop_index = [None, None, None, None]
       
        # Serial Connect
        # self.ser = serial.Serial("/dev/erp42", 115200) # Real World        
        self.ser = serial.Serial("/dev/ttyUSB0", 115200) # Simulation


        # ROS Publish
        rospy.init_node("Serial_IO", anonymous=False)
        self.serial_pub = rospy.Publisher("/serial", Serial_Info, queue_size=1)
       
        # Messages/Data
        self.serial_msg = Serial_Info()  # Message o publish
        self.alive = 0

        # Subscribing Ego information
        rospy.Subscriber("/local_msgs", Local, self.localcallback)

        # Subscribing Obstacle information
        rospy.Subscriber("/pcd", PoseArray, self.obstaclecallback)

        # Declaration
        self.ego_info = Local()
        self.control_input = Control_Info()

        # Reading Global Path
        self.read_global_path()

        # self.obstacle_info = PoseArray()
        self.obstacle_info_x = 0
        self.obstacle_info_y = 0

        # Pure Pursuit coefficient
        # self.lookahead_default = 10
        self.lookahead_default = 1
        self.ego_index = None

        # Stop coefficient
        self.stop_index_coefficient = 10
        self.brake_coefficient = 6

        # Serial Read Thread
        th_serialRead = threading.Thread(target=self.serialRead)
        th_serialRead.daemon = True
        th_serialRead.start()

        # rospy Rate
        self.rt = 20
        
        # Value reset to 0 for start
        self.setValue(0,0,0)

    def run(self):
        plot_cnt = 0
        timer_cnt = 5
        rate = rospy.Rate(self.rt)
        i = 0
        self.ego_index_pre = self.ego_index



        while not rospy.is_shutdown():
        
            print('ego info x : ', self.ego_info.x)
            print('ego info y : ', self.ego_info.y)
    
            self.obj_x = self.global_path_x[self.stop_index[i]]
            self.obj_y=  self.global_path_y[self.stop_index[i]]

            plot_cnt += 1

            self.setValue(10, self.pure_pursuit(), 0)

            self.stop_at_target_index(self.stop_index[i])
            if self.stop_index[i]+2 >= self.ego_index >= self.stop_index[i]-2: #and stop_bool == False:
                timer_cnt -= 1/self.rt

            

            if timer_cnt < 4.95000001:
                self.setValue(0,0,100)
                if abs(timer_cnt) < 0.00001:
                    #stop_bool = True
                    timer_cnt = 5
                    i+=1
                    self.plot_graph(i) # Everything
                    # self.plot_velocity_graph("Velocity_graph_{}".format(i)) # velocity graph
                    
                print("######### timer_cnt : {} ############".format(timer_cnt))
            self.ego_speed.append
            ####### jj just for Demo #######
            if 3000 <= self.ego_index < 3500 and self.ego_index_pre != self.ego_index:
                a = self.global_path_x[self.ego_index]
                b = self.global_path_y[self.ego_index]
                self.local4error_x = self.ego_info.x
                self.local4error_y = self.ego_info.y
                if self.local4error_x != self.local4error_pre_x and self.local4error_pre_x != None:
                    _tmp = self.err_dist(int(self.local4error_pre_x),int(self.local4error_pre_y),int(self.local4error_x),int(self.local4error_y),int(a),int(b))
                    self.error_dist += _tmp
                    print("error distance : ",self.error_dist)
                    
            self.local4error_pre_x, self.local4error_pre_y = self.local4error_x, self.local4error_y
            self.ego_index_pre = self.ego_index
            if self.ego_index > 3500:
                final_error = self.error_dist/len(range(3000,3500))
                print("Final Error is : ", final_error)
            ################################


            
            # if self.ego_index == self.stop_index_2 and self.ego_info.speeed == 0:
            #     time.sleep(3)
            # else:
            #     self.stop_at_target_index(self.stop_index_2)

            
            # if self.ego_index == self.stop_index_3 and self.ego_info.speeed == 0:
            #     time.sleep(3)
            # else:
            #     self.stop_at_target_index(self.stop_index_3)
            self.serialWrite()
            

        
            ########################### print values ##############################
            print("current index is ", self.ego_index, "\n")
            print("obstacle x : ", self.obj_x)
            print("obstacle y : ", self.obj_y)
            # print("stop_index : ", self.stop_index_1)
            #######################################################################

            # plot
            if plot_cnt % (0.1*self.rt) == 0: # always per 0.1sec
                self.save_position()

                
            # cnt += 1
            # # if cnt % (50*self.rt) == 0: # activate after 50 second
            
            # if cnt_stop > 20 : # if cnt_stop is over 20 (2 seconds in stop_index+-50)
            #     self.plot_graph() # global path, current path, obstacle position
            #     self.plot_velocity_graph() # velocity graph
            #     break
            # else:
            #     pass # plot graph 

            rate.sleep()

    def serialRead(self):
        print("Serial_IO: Serial reading thread successfully started")

        while True:
            
            print(f"Serial_IO: Reading serial {self.alive}")

            packet = self.ser.read_until(b'\x0d\x0a')
            # print(len(packet))
            if len(packet) == 18:
                header = packet[0:3].decode()

                if header == "STX":
                    #auto_manual, e-stop, gear
                    (self.serial_msg.auto_manual,
                    self.serial_msg.emergency_stop,
                    self.serial_msg.gear) \
                    = struct.unpack("BBB", packet[3:6])
                    
                    #speed, steer
                    tmp1, tmp2 = struct.unpack("2h", packet[6:10])
                    self.serial_msg.speed = tmp1 / 10  # km/h

                    self.serial_msg.steer = tmp2 / 71  # degree


                    self.alive = struct.unpack("B", packet[15:16])[0]

                    self.serial_pub.publish(self.serial_msg)

    def serialWrite(self):
        #Min/Max Limit
        if self.control_input.speed > 20:
            self.control_input.speed = 20

        self.control_input.speed = max(0, min(self.control_input.speed, 20))

        if self.control_input.brake > 200:
            self.control_input.brake = 200

        result = struct.pack(  #
            ">BBBBBBHhBBBB",
            0x53,
            0x54,
            0x58,
            1, #always auto
            self.control_input.emergency_stop,
            self.control_input.gear,
            int(self.control_input.speed * 10),
            int(self.control_input.steer * 71),
            int(self.control_input.brake),
            self.alive,
            0x0D,
            0x0A
        )
        self.ser.write(result)

    def localcallback(self, msg):
        self.ego_info.x = msg.x
        self.ego_info.y = msg.y
        self.ego_info.heading = msg.heading
        self.ego_info.speeed = msg.speeed
        ### for inside test
        # self.ego_info.x = self.global_path_x[100]
        # self.ego_info.y = self.global_path_y[100]
        # self.ego_info.heading = 110
        
    def obstaclecallback(self,msg):
        if msg.poses[0].orientation.z == 100:
            pass
        else:
            self.obstacle_info_x = msg.poses[0].orientation.x # relative coordinate obstacle x
            self.obstacle_info_y = msg.poses[0].orientation.y # relative coordinate obstacle y
            self.find_obstacle()
            # self.stop_index = self.target_index()
            # self.stop_index = 497
    
    def find_obstacle(self):
        # # for plot : jy
        # Lidar_x = self.ego_info.x + self.gps_to_Lidar*cos(np.radians(self.ego_info.heading))
        # Lidar_y = self.ego_info.y + self.gps_to_Lidar*sin(np.radians(self.ego_info.heading))
        l = sqrt((self.gps_to_Lidar + self.obstacle_info_x)**2 + (self.obstacle_info_y)**2) 
        self.obj_x = self.ego_info.x + l*cos(np.radians(self.ego_info.heading) - atan(self.obstacle_info_y/(self.obstacle_info_x + self.gps_to_Lidar))) 
        self.obj_y = self.ego_info.y + l*sin(np.radians(self.ego_info.heading) - atan(self.obstacle_info_y/(self.obstacle_info_x + self.gps_to_Lidar))) 
    
    def target_index(self):
        d = []
        dx = []
        dy = []
        for i in range(len(self.global_path_x)):
            dx.append(self.obj_x - self.global_path_x[i])
            dy.append(self.obj_y - self.global_path_y[i])
        
        for i in range(len(dx)):
            d.append(self.distance(dx[i], dy[i]))
        
        new_d = array(d)
        ind = argmin(new_d)
        self.dx = []
        self.dy = []
        
        return ind

    def read_global_path(self):
        # with open(f"/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/Inha_Songdo/right_curve.json", 'r') as json_file:
        with open(f"/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/kcity_simul/semi_map.json", 'r') as json_file:
        
            json_data = json.load(json_file)
            for _, (x, y, _, _) in enumerate(json_data.values()):
                self.global_path_x.append(x)
                self.global_path_y.append(y)

    def calc_distance(self, point_x, point_y):
        dx = self.ego_info.x - point_x
        dy = self.ego_info.y - point_y
        d = hypot(dx,dy)
        return d

    def distance(self, x, y):
        return sqrt(x**2+y**2)

    def search_ego_index(self):
        # if self.ego_index is None:
        d = []
        self.dx = []
        self.dy = []
        for i in range(len(self.global_path_x)):
            self.dx.append(self.ego_info.x - self.global_path_x[i])
            self.dy.append(self.ego_info.y - self.global_path_y[i])
        
        for i in range(len(self.dx)):
            d.append(self.distance(self.dx[i], self.dy[i]))
        
        new_d = array(d)
        ind = argmin(new_d)
        self.dx = []
        self.dy = []
        
        self.ego_index = ind
        # else:
        #     ind = self.ego_index
        #     distance_this_index = self.calc_distance(self.dx[ind], self.dy[ind])
        #     while True:
        #         distance_next_index = self.calc_distance(self.global_path_x[ind + 1], self.global_path_y[ind + 1])
        #         if distance_this_index < distance_next_index:
        #             break
        #         print("going to next point")
        #         ind = ind + 1 if (ind + 1) < len(self.global_path_x) else ind
        #         distance_this_index = distance_next_index
        
        #     self.ego_index = ind

        Lf = self.k * self.ego_info.speeed + self.lookahead_default  # update look ahead distance

        # search look ahead target point index
        while Lf > self.calc_distance(self.global_path_x[ind], self.global_path_y[ind]):
            if (ind + 1) >= len(self.global_path_x):
                break  # not exceed goal
            ind += 1

        return ind, Lf

    def pure_pursuit(self):
        ind,Lf=self.search_ego_index()
        lookahead = min(Lf, 6)
        target_index = ind  #self.ego_info.x'''''' + 49
        
        target_x, target_y = self.global_path_x[target_index], self.global_path_y[target_index]
        tmp = degrees(atan2(target_y - self.ego_info.y,
                            target_x - self.ego_info.x)) % 360

        alpha = self.ego_info.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)
        if degrees(angle) < 0.5 and degrees(angle) > -0.5:
            angle = 0
        tmp_steer = degrees(angle) 
        if abs(tmp_steer) > 5: 
            tmp_steer *= 0.8

        steer = max(min(tmp_steer, 27.0), -27.0) 
        return steer

    def plot_global_path(self, title):
        plt.figure(0)
        plt.plot(self.global_path_x,self.global_path_y,'k-',label='global_path')
        # plt.grid()
        # plt.legend()
        plt.savefig(title)

    def plot_graph(self, i):
        plt.figure(i+1)
        plt.plot(self.global_path_x,self.global_path_y,'k-',label='global_path')
        plt.plot(self.curPosition_x,self.curPosition_y,'ro',label='present_route',ms=2)
        plt.plot(self.objPosition_x,self.objPosition_y,'bo',label='obstacle_position')
        plt.grid()
        plt.legend(loc="lower right")
        plt.title("Coordinate System : GPS(ENU)")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig("Current_path_{}".format(i))

        t = 0.5

        for j in range(len(self.curPosition_x)//5-1):
            dx = self.curPosition_x[5*(j+1)]-self.curPosition_x[5*j]
            dy = self.curPosition_y[5*(j+1)]-self.curPosition_y[5*j]
            self.velocity.append(hypot(dx,dy)/t)
        
        graph_time = arange(0,len(self.velocity)/2,t)

        plt.figure(i+200)
        plt.plot(graph_time, self.velocity,)
        plt.title("Time-Velocity")
        plt.xlabel('time(s)')
        plt.ylabel('velocity(m/s)')
        plt.grid()
        plt.savefig("Velocity_{}".format(i))
        self.velocity = []
        

    def stop_at_target_index(self, target_index): # not proved
        if target_index is not None:
            # if self.ego_index >= target_index - self.stop_index_coefficient:
            if target_index - 30 >= self.ego_index >= target_index - 60:
                # self.setValue(self.ego_info.speeed, 0, self.ego_info.speeed*self.brake_coefficient)
                # self.setValue(self.control_input.speed, 0, self.ego_info.speeed*self.brake_coefficient)
                self.setValue(8, self.control_input.steer, 5)
                print("Trying to stop(FAR)")
                print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
            # if self.ego_index >= target_index:
            elif target_index - 10 > self.ego_index >= target_index - 30:
                self.setValue(3, self.control_input.steer, 0)
                print("Trying to stop(CLOSE)")
                print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
            elif target_index - 1 > self.ego_index >= target_index - 10:
                self.setValue(1, self.control_input.steer, 0)
                print("Trying to stop(CLOSE)")
                print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
            elif target_index + 1 >= self.ego_index >= target_index - 1:
                self.setValue(0, self.control_input.steer, 50)
                print("Trying to stop(VERY CLOSE)")
                print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
            else:
                pass
      
    ############################ jy ###############################
    # def stop_smooth(self, target_index):
    #     if target_index is not None:
    #         if target_index - 150


    # def smooth_brake(self, speed):
    #     t = 3
    #     h = 0.05
    #     a = speed/h
    #     ref_V = self.serial_msg.speed - h*a
    #     if self.serial_msg.speed > ref_V:
    #         self.setValue(0, self.control_input.steer, 30)
    #     elif self.serial_msg.speed < ref_V:
    #         self.setValue(10, self.control_input.steer, 0)
    #     else:
    #         pass
        
    ###############################################################
    # def stop_at_target_index(self, target_index): # not proved
    #     if target_index is not None:
    #         # if self.old_nearest_point_index >= target_index - self.stop_index_coefficient:
    #         if target_index - 10 >= self.old_nearest_point_index >= target_index - 60:
    #             # self.setValue(self.ego_info.speeed, 0, self.ego_info.speeed*self.brake_coefficient)
    #             # self.setValue(self.control_input.speed, 0, self.ego_info.speeed*self.brake_coefficient)
    #             self.setValue(0, self.control_input.steer, 5)
    #             print("Trying to stop(FAR)")
    #             print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
    #         # if self.old_nearest_point_index >= target_index:
    #         elif target_index-1 > self.old_nearest_point_index >= target_index - 20:
    #             self.setValue(3, self.control_input.steer, 15)
    #             print("Trying to stop(CLOSE)")
    #             print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
    #         elif self.old_nearest_point_index >= target_index:
    #             self.setValue(0, self.control_input.steer, 50)
    #             print("Trying to stop(CLOSE)")
    #             print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
    #         else:
    #             pass

    def setValue(self, speed, steer, brake):
        self.control_input.speed = speed
        self.control_input.steer = steer
        self.control_input.brake = brake

    def save_position(self):
        self.curPosition_x.append(self.ego_info.x)
        self.curPosition_y.append(self.ego_info.y)
        self.objPosition_x.append(self.obj_x)
        self.objPosition_y.append(self.obj_y)

    def err_dist(self,x1,y1,x2,y2,a,b):
        # area = abs((x1-a) * (y2-b)- (y1-b) * (x2-a))
        # AB = ((x1-x2)**2 + (y1-y2)**2) ** 0.5
        # distance = area/AB
        # return distance  # two ego index -> x,y // global path -> a,b
        dx1 = abs(a-x1)
        dy1 = abs(b-y1)
        dx2 = abs(a-x2)
        dy2 = abs(b-y2)
        distance1 = self.distance(dx1,dy1)
        distance2 = self.distance(dx2,dy2)
        error = (distance1+distance2)/2
        return error



if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    erp = Serial_IO().run()
