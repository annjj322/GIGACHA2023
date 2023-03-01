#!/usr/bin/env python3
import threading
import rospy
from time import sleep
from math import hypot
from std_msgs.msg import Int64
from local_pkg.msg import Serial_Info
from .cubic_spline_planner import calc_spline_course

class MP(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        rospy.Subscriber('/Displacement_right', Int64, self.encoderCallback)
        rospy.Subscriber('/serial', Serial_Info, self.serialTopulse)
        self.period = 1.0 / rate
        self.global_path = parent.shared.global_path
        self.shared = parent.shared

        self.ego = parent.shared.ego

        self.right = 0  # pulse from sensor
        self.left = 0  # pulse from serial

        # for odometry
        self.init = 0
        self.flag_filter = True

        self.left_pulse = 0
        self.right_pulse = 0
        self.pulse = 0
        self.diff_left = 0
        self.diff_right = 0
        self.temp = 0

        self.init_switch = False
        self.stop_thread = False
        self.right_switch = False
        self.collision_switch = False

        # for collision checker
        self.gear = int()
        self.auto_manual = int()
        self.backward_distance = int(0)
        self.init_dis = 0.0

        self.temp_x = []
        self.temp_y = []
        self.temp_dis = []

    def serialTopulse(self, data):
        self.gear = data.gear
        self.auto_manual = data.auto_manual

        if self.init == 0: 
            self.init = int(data.encoder[0]) + int(data.encoder[1])*256 \
                 + int(data.encoder[2])*256**2 + \
                    int(data.encoder[3])*256**3 
 
        self.left = int(data.encoder[0]) + int(data.encoder[1])*256 \
             + int(data.encoder[2])*256**2 + \
                int(data.encoder[3])*256**3 - self.init 

    def filter(self):
        if self.flag_filter:
            self.left_pulse = self.left
            self.right_pulse = self.right
            self.flag_filter = False

        if (abs(self.left - self.left_pulse) > 100):
            self.left_pulse = self.left + self.diff_left
        else:
            self.diff_left = self.left - self.left_pulse
            self.left_pulse = self.left

        if (abs(self.right - self.right_pulse) > 100):
            self.right_pulse = self.right + self.diff_right
        else:
            self.diff_right = self.right - self.right_pulse
            self.right_pulse = self.right

    def encoderCallback(self, msg):
        if self.right_switch == False:
            self.right_init = msg.data
            self.right_switch = True

        self.right = msg.data - self.right_init

        self.pulse = (self.right_pulse + self.left_pulse) / 2
        
        self.filter()
        
    def map_maker(self):
        if self.init_switch == False:
            self.init_switch = True
            self.init_x, self.init_y = self.ego.x, self.ego.y
            self.temp_x.append(self.init_x)
            self.temp_y.append(self.init_y)

        # self.global_path.x.append(self.ego.x)
        # self.global_path.y.append(self.ego.y)
        dis = hypot(self.temp_x[-1]- self.ego.x, self.temp_y[-1]- self.ego.y)

        if dis >= 0.1:
            self.temp_x.append(self.ego.x)
            self.temp_y.append(self.ego.y)

        self.temp = self.pulse

    def map_routine(self, value):

        self.global_path.x, self.global_path.y, _, self.global_path.curvature, _ = calc_spline_course(self.temp_x, self.temp_y, ds=0.1)
        
        
        x = []
        y = []

        x.append(self.global_path.x[-value])
        x.append(self.global_path.x[-1])
        x.append(self.global_path.x[value*2])

        y.append(self.global_path.y[-value])
        y.append(self.global_path.y[-1])
        y.append(self.global_path.y[value*2])

        cx, cy, _, _, _ = calc_spline_course(x, y, ds=0.1)

        self.global_path.x = self.global_path.x[value*2 + 1 : -value]
        self.global_path.y = self.global_path.y[value*2 + 1 : -value]

        self.global_path.x.extend(cx)
        self.global_path.y.extend(cy)

        param_check = 0

        for i in range(len(self.temp_x)-1):
            dis = hypot(self.temp_x[i+1]- self.temp_x[i],self.temp_y[i+1]- self.temp_y[i] )
            if dis <= 0.1:
                param_check += 1
            self.temp_dis.append(dis)

        print(self.temp_dis)
        print(param_check)
        print(self.global_path.curvature)
        

        # void_x =[]
        # void_y =[]
        # void_cur = []

        # while len(self.temp_x) >= 10:
        #     graph_x = self.temp_x[:10]
        #     graph_y = self.temp_y[:10]
        #     self.temp_x = self.temp_x[10:]
        #     self.temp_y = self.temp_y[10:]

        #     void_x, void_y, _, void_cur, _ = calc_spline_course(graph_x, graph_y, ds=0.1)
        #     self.global_path.x.extend(void_x)
        #     self.global_path.y.extend(void_y)
        #     self.global_path.curvature.extend(void_cur)

        # if len(self.temp_x) != 0:
        #     graph_x = self.temp_x
        #     graph_y = self.temp_y
        #     void_x, void_y, _, void_cur, _ = calc_spline_course(graph_x, graph_y, ds=0.1)
        #     self.global_path.x.extend(void_x)
        #     self.global_path.y.extend(void_y)
        #     self.global_path.curvature.extend(void_cur)
        
        print('11111111111')
        for i in range(3):
            self.global_path.x.extend(self.global_path.x)
            self.global_path.y.extend(self.global_path.y)
        print('2222222222222')

    # def map_routine(self, value):
    #     x = []
    #     y = []

    #     x.append(self.global_path.x[-value])
    #     x.append(self.global_path.x[-1])
    #     x.append(self.global_path.x[value*2])

    #     y.append(self.global_path.y[-value])
    #     y.append(self.global_path.y[-1])
    #     y.append(self.global_path.y[value*2])

    #     cx, cy, _, _, _ = calc_spline_course(x, y, ds=0.12)

    #     self.global_path.x = self.global_path.x[value*2 + 1 : -value]
    #     self.global_path.y = self.global_path.y[value*2 + 1 : -value]

    #     self.global_path.x.extend(cx)
    #     self.global_path.y.extend(cy)

    #     # self.global_path.x, self.global_path.y, _, self.global_path.curvature, _ = calc_spline_course(self.global_path.x, self.global_path.y, ds=0.1)
        
    #     print('11111111111')
    #     for i in range(3):
    #         self.global_path.x.extend(self.global_path.x)
    #         self.global_path.y.extend(self.global_path.y)
    #     print('2222222222222')

    def map_remover(self):
        if not self.collision_switch:
            self.init_dis = self.ego.distance
            self.collision_switch = True

        if self.gear == 2:
            self.backward_distance = int(self.ego.distance - self.init_dis)

    def run(self):
        while True:
            if not self.stop_thread:
                if round(self.pulse) % 6 == 0 and self.pulse !=self.temp:
                    self.map_maker()
                
                if self.auto_manual == 0:
                    self.map_remover()
                    if self.auto_manual == 1:
                        self.temp_x = self.temp_x[:-10*self.backward_distance]
                        self.temp_y = self.temp_y[:-10*self.backward_distance]
                        break                        

                if len(self.temp_x) >= 50 :
                    if hypot(self.ego.x - self.temp_x[0], self.ego.y - self.temp_y[0]) <= 10:
                        for i in range(10):
                            dis = hypot(self.ego.x - self.temp_x[i], self.ego.y - self.temp_y[i])
                            if dis <= 3:
                                self.temp_x = self.temp_x[i:]
                                self.temp_y = self.temp_y[i:]
                                self.stop_thread = True
                                self.map_routine(5)
                                print('====================2ND START====================')
                                self.shared.state = "2nd"
                                break


            else:
                sleep(self.period)