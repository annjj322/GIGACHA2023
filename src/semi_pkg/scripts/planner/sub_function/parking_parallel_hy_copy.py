import numpy as np
from .cubic_spline_planner import main
import math
import threading
import pymap3d
import json
from shared.path import Path
from math import cos,  radians, sin, atan2, sqrt, hypot,asin,tan
from numpy import rad2deg, argmin, hypot,linspace,degrees
from .convert_view import convert_coord
import csv


class parallel_traj_hy():
    def __init__(self, sh, pl, eg,park):
        self.shared = sh
        self.plan = pl
        self.ego = eg
        self.parking = park
        self.global_path = self.shared.global_path
        
        self.p0=[74.83,83.24]#reg
        self.p1=[72.46,78.88]#leg 
        self.m2=0#세로가 이루는 예각
        self.m=0#가로가 이루는 둔각 
        self.n1a=0#leg 점에서 여유 
        self.n1b=0#
        self.n11a=0#
        self.n11b=0#
        self.f_x=[]
        self.f_y=[]
        self.x1=[]
        self.y1=[]
        self.x=[]
        self.y=[]
        self.flag=True
        self.r2=2.8
        self.r=2.8
        self.save_index=0
        self.flag_1=True
        self.exit_flag=True
        self.perception_flag=True
        self.park_lock = threading.Lock()
    
    def data_storage(self): 
     
        if self.flag_1:    
            self.park_lock.acquire()
            # if len(self.shared.perception.edge_L) != 0: 
            #     '''do you want field test using perception information, uncomment above line and press TAB below lines'''
            #     vec_L = [self.shared.perception.edge_L[0], self.shared.perception.edge_L[1]]
            #     vec_R = [self.shared.perception.edge_R[0], self.shared.perception.edge_R[1]]
            #     print("rew L:", vec_L)
            #     print("rew R:", vec_R)
            #     self.Ledge_camera = convert_coord(angle=270, vec=vec_L, offset=[0.2,1.03])
            #     self.Redge_camera = convert_coord(angle=270, vec=vec_R, offset=[0.2,1.03])

            #     self.p0 = convert_coord(angle=(self.ego.heading+360-90)%360, vec=self.Ledge_camera, offset=[self.ego.x, self.ego.y])
            #     self.p1 = convert_coord(angle=(self.ego.heading+360-90)%360, vec=self.Redge_camera, offset=[self.ego.x, self.ego.y])
            # self.p1 = [12.8, 15.1] #  parellel
            # self.p0 = [16.06, 19.24]    
            # self.p1 = [9.6473, 11.075] #  parellel
            # self.p0 = [12.844, 15.1823] 
            m2=atan2((self.p1[1]-self.p0[1]),(self.p1[0]-self.p0[0]))# 세로가 이루는 예각
            self.m2=self.make_yegak(m2)
            m=atan2(-(self.p1[0]-self.p0[0]),(self.p1[1]-self.p0[1])) #가로가 이루는 둔각 
            if np.degrees(m)<0:
                m+=np.pi
                m=m%(2*np.pi)
            self.m=m
            #####현재 안쓰는중########
            d100 = hypot((self.ego.x-self.p0[0]),(self.ego.y-self.p0[1]))
            alpha = atan2((self.ego.y-self.p0[1]),(self.ego.x-self.p0[0]))
            alpha = self.make_yegak(alpha)
            # print('d100',d100)
            # print('alpha',np.degrees(alpha))
            #######################################
            self.n11a = 1.1#(d100 * abs(sin((alpha-m2))))
            self.n11b = 0.5*self.n11a
            self.save_index = self.ego.index + 40  
            print('save index',self.save_index)
            self.flag_1 = False
            self.park_lock.release()
        
    def making_forward_path(self):
        self.data_storage()
        self.making_trajectory()
        first_path_x=[self.ego.x,self.global_path.x[self.save_index+40]]
        first_path_y=[self.ego.y,self.global_path.y[self.save_index+40]]
        fx,fy=main(first_path_x,first_path_y)
        self.trans_global_path(fx,fy)
  
   
    def backward_path(self):
        self.trans_global_path(self.f_x,self.f_y)
    
    def making_trajectory(self):
        if self.flag:    
            # p0가 REG, p1이 LEG
            n1x = self.p0[0] - self.n11a*cos(self.m) - self.n11b * cos(self.m2) # reg점에서  
            n1y = self.p0[1] - self.n11a*sin(self.m) - self.n11b * sin(self.m2)
            #####################################
            d = 1
            inc=atan2(d,self.r)
            inc=self.make_yegak(inc)
            inc*=2
            n1=int((np.pi/(math.asin(1/(20*self.r)))))
            n2=int((np.pi/(math.asin(1/(20*self.r2)))))
            ####################################
            d52=hypot((self.global_path.x[self.save_index]-n1x),(self.global_path.y[self.save_index]-n1y))
            d100=sqrt(d52**2-self.r2**2)
            inc2=asin(self.r2/d52)
            inc2=self.make_yegak(inc2)
            ##################################
            inc3=atan2((n1y-self.global_path.y[self.save_index]),(n1x-self.global_path.x[self.save_index]))  
            inc3=self.make_yegak(inc3) 
            ####################################
            ##############################
            tot_inc=inc2+inc3            
            #############################
            inter_x=self.global_path.x[self.save_index] - d100 * cos(np.pi-tot_inc)
            inter_y=self.global_path.y[self.save_index] + d100 * sin(np.pi-tot_inc)
            tmtm=atan2(-1,tan(tot_inc))
            tmtm=self.make_yegak(tmtm)
            tmtm+=np.pi
            #######실험실###################
            x_new=(self.global_path.y[self.save_index] - tan(tot_inc)*self.global_path.x[self.save_index] + tan(self.m2) * (self.p0[0]) - self.p0[1])/(tan(self.m2-tan(tot_inc)))
            y_new=tan(self.m2)*x_new -tan(self.m2) * self.p0[0] + self.p0[1]
            tmp_inc=atan2((n1y-y_new),(n1x-x_new))
            inc_new=self.make_yegak(tmp_inc)
            #################고정#####################
            x=[]
            y=[]
            for j in range(360): #reg 점 근처 
                if self.m<=j*2*np.pi/360<=np.pi+inc_new:#tmtm
                    x.append(n1x+self.r2*cos(j*2*np.pi/360)) 
                    y.append(n1y+self.r2*sin(j*2*np.pi/360))    
            ##########################################
            ##########평행이동만######################
            n2x=self.global_path.x[self.save_index]- 1 * cos(self.m2) - self.r * cos(0.5*np.pi - self.m2)
            n2y=self.global_path.y[self.save_index]- 1 * sin(self.m2) + self.r * sin(0.5*np.pi - self.m2)

            for i in range(360): #leg 모서리     
                if 0<=(i*2*np.pi/360)<=inc: 
                    self.x1.append(n2x + self.r*cos(i*2*np.pi/360-(np.pi-abs(self.m))))
                    self.y1.append(n2y + self.r*sin(i*2*np.pi/360-(np.pi-abs(self.m))))
            ############################################
            x=x[::-1]
            y=y[::-1]
            tmpp_x,tmpp_y=main((self.x1[-1],x_new),(self.y1[-1],y_new))
            # tmpp_x,tmpp_y=main((self.x1[-1],inter_x),(self.y1[-1],inter_y))
            # forward_x,forward_y=main((self.global_path.x[self.save_index]- 2 * cos(self.m2),self.global_path.x[self.save_index]- 1 * cos(self.m2)),(self.global_path.y[self.save_index] - 2 * sin(self.m2) ,self.global_path.y[self.save_index]- 1 * sin(self.m2)))
            forward_x,forward_y=main((self.global_path.x[self.save_index]- 10 * cos(self.m2),self.x1[0]),(self.global_path.y[self.save_index] - 10 * sin(self.m2) ,self.y1[0]))
            self.f_x= forward_x + self.x1 + tmpp_x + x 
            self.f_y= forward_y + self.y1 + tmpp_y + y 
            self.flag=False
    
    def exit(self):
        if self.exit_flag:
            self.f_x=self.f_x[::-1]
            self.f_y=self.f_y[::-1]
            self.exit_flag=False
        
        self.global_path.x=self.f_x
        self.global_path.y=self.f_y
    
    # def make_yegak(self,angle):
    #     result = abs(angle)%(np.pi)
    #     return result
    
    def make_yegak(self,angle):
        if abs(np.degrees(angle))>90:
            angle=np.pi-abs(angle)
            angle=angle%(2*np.pi)
        else:
            angle=abs(angle)
            angle=angle%(2*np.pi)
        return angle   
    
    def trans_global_path(self,x,y):
        self.global_path.x=x
        self.global_path.y=y
        self.global_path.mission = []
        for i in range(len(self.global_path.x)):
            self.global_path.mission.append("parking")

            