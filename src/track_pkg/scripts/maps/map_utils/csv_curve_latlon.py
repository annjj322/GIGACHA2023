#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymap3d as pm
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import sys
from cubic_spline_planner import calc_spline_course


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
base_lat = 37.36458356
base_lon = 126.7237789
base_alt = 15.4

# simul
# base_lat = 37.239235
# base_lon = 126.77315833333333
# base_alt = 15.4

# yonghyeon_navileguan
# base_lat = 37.4508561
# base_lon = 126.6492464
# base_alt = 15.4


def get_xy(lat, lon, alt):  # 점들 사이의 새로운 점들을 설정
    e, n, u = pm.geodetic2enu(lat, lon, alt, base_lat, base_lon, base_alt)
    print("hello")
    return e, n

def enu(name, num):
    colnames = ['lon', 'lat']
    df = pd.read_csv(f'gpp2.csv', names=colnames, header=None)
    x = []
    y = []

    for i in range(num):  # i=1,2,3,...
        latitude = df.loc[i, 'lat'].tolist()
        longitude = df.loc[i, 'lon'].tolist()  # 0 행 부터라서 index 1씩 빼줌
        output = get_xy(latitude, longitude, 0.5)
        x.append(output[0])
        y.append(output[1])
    save_data = list(zip(x, y))
    save_df = pd.DataFrame(save_data)
    save_df.to_csv('%s.csv' % name, index=False, header=False)
    print(f"Map saved to maps/{name}.csv")
    plt.scatter(x, y)
    plt.show()


def cubic(name, *args):  # args에는 1,2,3,4,5,6 등 막 들어 수있음

    colnames = ['lon', 'lat']
    # df = pd.read_csv(f'maps/Siheung/nodes/turn_right/turn_right_line.csv', names=colnames, header=None) # siheung
    df = pd.read_csv(f'points.csv', names=colnames, header=None)
    x = []
    y = []

    for i in args:  # i=1,2,3,...
        latitude = df.loc[i-1, 'lat'].tolist()
        longitude = df.loc[i-1, 'lon'].tolist()  # 0 행 부터라서 index 1씩 빼줌
        output = get_xy(latitude, longitude, 0.5)
        x.append(output[0])
        y.append(output[1])

    cx, cy, cyaw, ck, s = calc_spline_course(x, y, ds=0.1)
    save_data = list(zip(cx, cy, cyaw, ck, s))

    save_df = pd.DataFrame(save_data)
    # save_df.to_csv('maps/Siheung/maps/right/%s.csv'%name, index=False, header = False) # siheung
    save_df.to_csv('%s.csv' % name, index=False, header=False)
    print(f"Map saved to maps/{name}.csv")
    plt.scatter(cx, cy)
    plt.show()

    return(cx, cy, cyaw, ck, s)






# cubic("left2", 2, 3, 4, 5, 6, 7, 8, 9, 10)
# cubic("str1", 1, 2)
# cubic("str2", 3, 4)
# cubic("str3", 5, 6)
# cubic("parksssang1", 1,2,3)
# cubic("kcitySTR",1,2)
# enu('curve1', 842)
# enu('curve2', 449)
enu('curve3', 282)

# cubic("2",2,3,4,5,6,7)
# cubic("3",7,8)