#!/usr/bin/env python3
from sig_int_handler import Activate_Signal_Interrupt_Handler
import serial
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from local_pkg.msg import Local
import threading
import struct
import rospy
from math import sqrt, atan2, sin
from numpy import degrees, radians, hypot, array, argmin
import json
import matplotlib.pyplot as plt

class Serial_IO:
    def __init__(self):
        self.k = 0.55
        self.WB = 1.04 # wheel base

        # Global Path
        self.global_path_x = []
        self.global_path_y = []

        # Ego information      
        self.curPosition_x = []
        self.curPosition_y = []
        self.velocity = []

        # Serial Connect
        self.ser = serial.Serial("/dev/erp42", 115200) # Real World

        # ROS Publish
        rospy.init_node("Serial_IO", anonymous=False)
        self.serial_pub = rospy.Publisher("/serial", Serial_Info, queue_size=1)
       
        # Messages/Data
        self.serial_msg = Serial_Info()  # Message o publish
        self.alive = 0

        # Subscribing Ego information
        rospy.Subscriber("/local_msgs", Local, self.localcallback)

        # Reading Global Path
        self.read_global_path()

        # Declaration
        self.ego_info = Local()
        self.control_input = Control_Info()

        # Pure Pursuit coefficient
        self.lookahead_default = 10
        self.old_nearest_point_index = None

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
        cnt = 0
        rate = rospy.Rate(self.rt)

        # show global path
        self.plot_global_path()

        while not rospy.is_shutdown():
            print("current index is ", self.old_nearest_point_index, "\n")
            self.setValue(8, self.pure_pursuit(), 0)
            self.stop_at_target_index(1060) # end point is 1072
            self.serialWrite()
            
            if cnt % (0.1*self.rt) == 0: # always per 0.1sec
                self.save_position()
                
            cnt += 1
            rate.sleep()
            if cnt % (60*self.rt) == 0:
                self.plot_present_route()



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

    def localcallback(self,msg):
        self.ego_info.x = msg.x
        self.ego_info.y = msg.y
        self.ego_info.heading = msg.heading
        self.ego_info.speeed = msg.speeed
        
    def read_global_path(self):
        with open(f"/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/Inha_Songdo/right_curve.json", 'r') as json_file:
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

    def search_target_index(self):
        # if self.old_nearest_point_index is None:
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
        
        self.old_nearest_point_index = ind
        # else:
        #     ind = self.old_nearest_point_index
        #     distance_this_index = self.calc_distance(self.dx[ind], self.dy[ind])
        #     while True:
        #         distance_next_index = self.calc_distance(self.global_path_x[ind + 1], self.global_path_y[ind + 1])
        #         if distance_this_index < distance_next_index:
        #             break
        #         print("going to next point")
        #         ind = ind + 1 if (ind + 1) < len(self.global_path_x) else ind
        #         distance_this_index = distance_next_index
        
        #     self.old_nearest_point_index = ind

        Lf = self.k * self.ego_info.speeed + self.lookahead_default  # update look ahead distance

        # search look ahead target point index
        while Lf > self.calc_distance(self.global_path_x[ind], self.global_path_y[ind]):
            if (ind + 1) >= len(self.global_path_x):
                break  # not exceed goal
            ind += 1

        return ind, Lf

    def pure_pursuit(self):
        ind,Lf=self.search_target_index()
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

    def plot_global_path(self):
        plt.figure(0)
        plt.plot(self.global_path_x,self.global_path_y,'k-',label='global_path')
        plt.grid()
        plt.legend()
        plt.show()

    def plot_present_route(self):
        plt.figure(1)
        plt.plot(self.global_path_x,self.global_path_y,'k-',label='global_path')
        plt.plot(self.curPosition_x,self.curPosition_y,'ro',label='present_route',ms=2)
        plt.grid()
        plt.legend()
        plt.show()

    def velocity_graph(self):
        t = 0.5
        for i in range(len(self.curPosition_x)//5-1):
            dx = self.curPosition_x[5*(i+1)]-self.curPosition_x[5*i]
            dy = self.curPosition_y[5*(i+1)]-self.curPosition_y[5*i]
            self.velocity.append(hypot(dx,dy)/t)
        
        graph_time = range(len(self.velocity)*2)

        plt.figure(1)
        plt.plot(self.velocity,graph_time)
        plt.xlabel('time(x)')
        plt.ylabel('velocity(m/s)')
        plt.show()

    def stop_if_end(self): # not proved
        if self.old_nearest_point_index == len(self.global_path_x):
            self.setValue(0, 0, 45)
            print("STOPPING.........")

    def stop_at_target_index(self, target_index): # not proved
        # if self.old_nearest_point_index >= target_index - self.stop_index_coefficient:
        if target_index - 10 >= self.old_nearest_point_index >= target_index - 60:
            # self.setValue(self.ego_info.speeed, 0, self.ego_info.speeed*self.brake_coefficient)
            # self.setValue(self.control_input.speed, 0, self.ego_info.speeed*self.brake_coefficient)
            self.setValue(0, self.control_input.steer, 5)
            print("Trying to stop(FAR)")
            print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
        # if self.old_nearest_point_index >= target_index:
        elif target_index-1 > self.old_nearest_point_index >= target_index - 20:
            self.setValue(3, self.control_input.steer, 15)
            print("Trying to stop(CLOSE)")
            print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
        elif self.old_nearest_point_index >= target_index:
            self.setValue(0, self.control_input.steer, 50)
            print("Trying to stop(CLOSE)")
            print("(Speed, Steer, Brake): {}, {}, {}".format(self.control_input.speed, self.control_input.steer, self.control_input.brake))
        else:
            pass

    def setValue(self, speed, steer, brake):
        self.control_input.speed = speed
        self.control_input.steer = steer
        self.control_input.brake = brake

    def save_position(self):
        self.curPosition_x.append(self.ego_info.x)
        self.curPosition_y.append(self.ego_info.y)
        print(1)


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    erp = Serial_IO().run()
