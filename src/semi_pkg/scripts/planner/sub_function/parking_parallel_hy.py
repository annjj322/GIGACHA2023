import numpy as np
from .cubic_spline_planner import main
import math

import pymap3d
import json
from shared.path import Path
from math import cos, degrees, radians, sin, atan2, sqrt, hypot
from numpy import rad2deg, argmin, hypot,linspace
import csv


class parallel_traj_hy():
    def __init__(self, sh, pl, eg,park):
        self.shared = sh
        self.plan = pl
        self.ego = eg
        self.parking = park
        self.global_path = self.shared.global_path
        
        self.p0=[74.83,83.24]#lidar에서 받아오기, 직접 적자
        self.p1=[72.46,78.88]
        self.m2=1.0804883694194916 # 세로가 이루는 예각
        self.m=2.0692557372615763 #가로가 이루는 둔각 
        self.r=2.29
        self.garo=2.914
        self.sero=5.03
        self.n1a=0.5 #가로 여유
        self.n1b=0.5 #세로 여유 
        self.x1=[]
        self.y1=[]
        self.x=[]
        self.y=[]
        self.jikjin_x=[]
        self.jikjin_y=[]
        self.p2x=self.p1[0]+self.garo * math.cos(self.m)
        self.p2y=self.p1[1]+self.garo * math.sin(self.m)
        self.p3x=self.p0[0]+self.garo * math.cos(self.m)
        self.p3y=self.p0[1]+self.garo * math.sin(self.m)
        self.cnt=False
        self.flag=True
        self.r2=0
        self.mmmm2=0
        self.making_trajectory()
        self.manuri_flag=True
        self.exit_flag=True
    def making_forward_path(self):
        
        first_path_x=[self.ego.x,self.x1[0]]
        first_path_y=[self.ego.y,self.y1[0]]
        fx,fy=main(first_path_x,first_path_y)
        print('cucucucuc',fx)
        # self.parking.forward_path.x=fx
        # self.parking.forward_path.y=fy
        self.global_path.x=fx
        self.global_path.y=fy
        # self.shared.parking_path_forward.x=fx
        # self.shared.parking_path_forward.y=fy
        
    
    def making_trajectory(self):
        if self.flag:    
            n1x=self.p0[0]-self.n1a*math.cos(self.m) - self.n1b*math.cos(self.m2)
            n1y=self.p0[1]-self.n1a*math.sin(self.m) - self.n1b*math.sin(self.m2)
            n2x=self.p1[0]-self.n1a*math.cos(self.m) + self.n1b*math.cos(self.m2)
            n2y=self.p1[1]-self.n1a*math.sin(self.m) + self.n1b*math.sin(self.m2)
            r2=(math.hypot((n2x-n1x),(n2y-n1y)))-self.r
            self.r2=r2
            d1y=n1y-n2y
            d1x=n1x-n2x
            self.mmmm2=math.atan2(d1y,d1x)
            n1=int((np.pi/(math.asin(1/(20*self.r)))))
            n2=int((np.pi/(math.asin(1/(20*r2)))))
            
            for i in range(360): #두번째 모서리 
                if not 2*(self.mmmm2)<=(i*2*np.pi/360)<=2*self.mmmm2 + 1.5*np.pi : 
                    self.x1.append(n2x + self.r*math.cos((i*2*np.pi/360)-self.mmmm2))
                    self.y1.append(n2y + self.r*math.sin((i*2*np.pi/360)-self.mmmm2))
            for j in range(360): #첫
                if self.mmmm2 + 0.5 * np.pi<=(j*2*np.pi/360)<=np.pi + self.mmmm2:
                    self.x.append(n1x+r2*math.cos(j*2*np.pi/360)) 
                    self.y.append(n1y+r2*math.sin(j*2*np.pi/360))    
            
            # self.x1=self.x1[::-1]
            # self.y1=self.y1[::-1]
            # self.x1,self.y1=main(self.x1,self.y1)
            self.x=self.x[::-1]
            self.y=self.y[::-1]
            # kkx,kky=main([self.x1[-1],self.x[0]],[self.y1[-1],self.y[0]])
            # self.x,self.y=main(self.x,self.y)
            # self.x1.extend(kkx)
            # self.y1.extend(kky)
            self.x1.extend(self.x)
            self.y1.extend(self.y)
            self.x1,self.y1=main(self.x1,self.y1)
            self.flag=False
        
    def parking_back_phase2(self):
        self.global_path.x=self.x1
        self.global_path.y=self.y1      
    
    def manuri(self):
        if self.manuri_flag:
            imimx=self.ego.x
            imimy=self.ego.y
            self.jikjin_x=[imimx,imimx-5*math.cos(self.m2)]
            self.jikjin_y=[imimy,imimy-5*math.sin(self.m2)]
            self.jikjin_x,self.jikjin_y=main(self.jikjin_x,self.jikjin_y)
            self.manuri_flag=False
        self.global_path.x=self.jikjin_x
        self.global_path.y=self.jikjin_y

    # def parking_back_phase(self):
    #     self.global_path.x = self.x
    #     self.global_path.y = self.y    
    #     self.ego.target_steer = -np.rad2deg(math.asin(1.04/self.r2))
    
    
    def parking_drive(self, direction): #0앞으로 , 2면 뒤로
        self.parking.direction = direction

        if self.parking.direction == 2:
            if self.cnt == False:
                self.parking.index = 0
                self.cnt = True
            #path = self.parking.backward_path
            path= self.global_path
        else:
            #path = self.parking.forward_path
            path = self.global_path
        self.parking.index = self.park_index_finder(path)
        self.parking.stop_index = len(path.x)
    
    def park_index_finder(self,path):
        min_dis = -1
        min_idx = 0
        step_size = 10
        save_idx = self.parking.index

        for i in range(max(self.parking.index - step_size, 0), self.parking.index + step_size):
            try:
                dis = math.hypot(
                    path.x[i] - self.ego.x, path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i

        return min_idx
    
    def exit(self):
        if self.exit_flag:
            imimx=self.ego.x
            imimy=self.ego.y
            self.jikjin_x=[imimx,imimx+5*math.cos(self.m2)]
            self.jikjin_y=[imimy,imimy+5*math.sin(self.m2)]
            self.jikjin_x,self.jikjin_y=main(self.jikjin_x,self.jikjin_y)
            
            self.x1=self.x1[::-1]
            self.y1=self.y1[::-1]
            self.exit_flag=False
        
        self.global_path.x=self.jikjin_x
        self.global_path.y=self.jikjin_y
      
  