#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymap3d as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from lib.cubic_spline_planner import calc_spline_course


# 송도
# base_lat = 37.383784   
# base_lon = 126.654310
# base_alt = 15.4

# 송도 건물 옆
# base_lat = 37.3851693 #새로운 베이스
# base_lon = 126.6562271
# base_alt = 15.4

# # songdo out
# base_lat = 37.3843177
# base_lon = 126.6553022
# base_alt = 15.4

# Siheung
# base_lat = 37.36458356
# base_lon = 126.7237789
# base_alt = 15.4

#simul
# base_lat = 37.239235 
# base_lon = 126.77315833333333
# base_alt = 15.4

#simul_kcity_sangwook
base_lat = 37.2389871166175 
base_lon = 126.772996046328
base_alt = 15.4

def get_xy(lat, lon, alt): #점들 사이의 새로운 점들을 설정 
    e, n, u = pm.geodetic2enu(lat, lon, alt, base_lat, base_lon, base_alt)
    return e, n

def cubic(name,*args): # args에는 1,2,3,4,5,6 등 막 들어 수있음

    colnames=['lon', 'lat']
    # df = pd.read_csv(f'maps/Siheung/nodes/turn_right/turn_right_line.csv', names=colnames, header=None) # siheung
    df = pd.read_csv(f'maps/kcity_simul/kcity_straight_lane.csv', names=colnames, header=None)
    x=[]
    y=[]
    
    for i in args: # i=1,2,3,...
        latitude = df.loc[i-1,'lat'].tolist() # 
        longitude = df.loc[i-1,'lon'].tolist() # 0 행 부터라서 index 1씩 빼줌
        output = get_xy(latitude, longitude, 0.5)
        x.append(output[0])
        y.append(output[1])

    cx, cy, cyaw, ck, s = calc_spline_course(x, y, ds=0.1)
    save_data = list(zip(cx, cy, cyaw, ck, s))

    save_df = pd.DataFrame(save_data)
    # save_df.to_csv('maps/Siheung/maps/right/%s.csv'%name, index=False, header = False) # siheung
    save_df.to_csv('maps/kcity_simul/%s.csv'%name, index=False, header = False) 
    print(f"Map saved to maps/{name}.csv")
    plt.scatter(cx, cy)    
    plt.show()

    return(cx, cy, cyaw, ck, s)

cubic("kcity_straight_lane!",1,2)
# cubic("2",2,3)
# cubic("3",3,4)
# cubic("4",4,5,6,7,8,9)
# cubic("5",9,10)