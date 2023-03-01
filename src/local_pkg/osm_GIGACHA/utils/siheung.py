import pymap3d as pm
import json
from math import hypot

# Siheung
base_lat = 37.36458356
base_lon = 126.7237789
base_alt = 15.4

lat_ = 37.3647666469637
lon_ = 126.723978519695

x_ = []
y_ = []


def get_xy(lat, lon, alt):  # 점들 사이의 새로운 점들을 설정
    e, n, u = pm.geodetic2enu(lat, lon, alt, base_lat, base_lon, base_alt)
    return e, n


def read_global_path():
    with open("siStraight.json", 'r') as json_file:
        json_data = json.load(json_file)
        for n, (x, y, mission) in enumerate(json_data.values()):
            x_.append(x)
            y_.append(y)


def index_finder():
    read_global_path()
    my_x, my_y = get_xy(lat_,lon_,0.5)

    i = 0
    idx = 0

    while True:
        dis = hypot(x_[i] - my_x, y_[i] - my_y)
        i += 1

        if dis <= 0.2:
            print(i)
            return i
            
            break




stop_index = index_finder()

print(stop_index)