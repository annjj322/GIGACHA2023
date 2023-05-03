"""
Linear MPC controller (X-Y frame)
author: huiming zhou
"""
from local_pkg.msg import Serial_Info
from local_pkg.msg import Local
import os
import sys
import math
import cvxpy
import numpy as np
import matplotlib.pyplot as plt
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from . import draw as draw
from . import cubic_spline as cs
import rospy

class P:
    # System config
    NX = 4  # state vector: z = [x, y, v, phi] * phi = yaw angle
    NU = 2  # input vector: u = [acceleration, steer]
    T = 20  # finite time horizon length

    # MPC config
    Q = np.diag([1.0, 1.0, 1.0, 1.0])  # penalty for states
    Qf = np.diag([1.0, 1.0, 1.0, 1.0])  # penalty for end state
    R = np.diag([0.01, 0.1])  # penalty for inputs
    Rd = np.diag([0.01, 0.1])  # penalty for change of inputs

    dist_stop = 5  # stop permitted when dist to goal < dist_stop
    speed_stop = 0.5 / 3.6  # stop permitted when speed < speed_stop
    time_max = 500.0  # max simulation time
    iter_max = 5  # max iteration
    target_speed = 15.0 * 3.6  # target speed
    N_IND = 10  # search index number
    dt = 0.05  # time step
    d_dist = 0.1  # dist step
    du_res = 0.1  # threshold for stopping iteration

    # vehicle config
    RF = 0.87  # [m] distance from rear to vehicle front end of vehicle
    RB = 0.49  # [m] distance from rear to vehicle back end of vehicle
    W = 0.90  # [m] width of vehicle
    WD = 0.965 * W  # [m] distance between left-right wheels
    WB = 1.04  # [m] Wheel base
    TR = 0.65  # [m] Tyre radius
    TW = 0.17  # [m] Tyre width

    steer_max = np.deg2rad(27.0)  # max steering angle [rad]
    steer_change_max = np.deg2rad(27.0)  # maximum steering speed [rad/s]
    speed_max = 20.0 / 3.6  # maximum speed [m/s]
    speed_min = -20.0 / 3.6  # minimum speed [m/s]
    acceleration_max = 1.0  # maximum acceleration [m/s2]



class Node:
    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.direct = 1 # 전진


    def update(self, a, delta): #가속도랑 조향각, 방향
        delta = self.limit_input_delta(delta) #최대 조향각 조절
        self.x += self.v * math.cos(self.yaw) * P.dt 
        self.y += self.v * math.sin(self.yaw) * P.dt
        self.yaw += self.v / P.WB * math.tan(delta) * P.dt
        self.direct = 1  
        self.v += self.direct * a * P.dt
        self.v = self.limit_speed(self.v)

    @staticmethod
    def limit_input_delta(delta):
        if delta >= P.steer_max:
            return P.steer_max

        if delta <= -P.steer_max:
            return -P.steer_max

        return delta

    @staticmethod
    def limit_speed(v):
        if v >= P.speed_max:
            return P.speed_max

        if v <= P.speed_min:
            return P.speed_min

        return v  

class PATH:
    def __init__(self, cx, cy, cyaw, ck):
        self.cx = cx
        self.cy = cy
        self.cyaw = cyaw
        self.ck = ck
        self.length = len(cx)
        self.ind_old = 0

    def nearest_index(self, node):
        """
        calc index of the nearest node in N steps
        :param node: current information
        :return: nearest index, lateral distance to ref point
        """

        dx = [node.x - x for x in self.cx[0 : -1]]
        dy = [node.y - y for y in self.cy[0 : -1]]
        dist = np.hypot(dx, dy)

        self.ind_old = int(np.argmin(dist))

        ind = self.ind_old

        return ind

def calc_ref_trajectory_in_T_step(node, ind, ref_path, sp):
    """
    calc referent trajectory in T steps: [x, y, v, yaw]
    using the current velocity, calc the T points along the reference path
    :param node: current information
    :param ref_path: reference path: [x, y, yaw]
    :param sp: speed profile (designed speed strategy)
    :return: reference trajectory
    """

    z_ref = np.zeros((P.NX, P.T + 1))
    length = ref_path.length

    z_ref[0, 0] = ref_path.cx[ind]
    z_ref[1, 0] = ref_path.cy[ind]
    z_ref[2, 0] = ref_path.cyaw[ind]
    z_ref[3, 0] = sp[ind]

    dist_move = 0.0

    for i in range(1, P.T + 1):
        dist_move += node.v * P.dt
        ind_move = int(round(dist_move / P.d_dist))
        index = min(ind + ind_move, length - 1)

        z_ref[0, i] = ref_path.cx[index]
        z_ref[1, i] = ref_path.cy[index]
        z_ref[2, i] = ref_path.cyaw[index]
        z_ref[3, i] = sp[index]

    return z_ref

def calc_speed_profile(cx, cy, cyaw, target_speed):
    """
    design appropriate speed strategy
    :param cx: x of reference path [m]
    :param cy: y of reference path [m]
    :param cyaw: yaw of reference path [m]
    :param target_speed: target speed [m/s]
    :return: speed profile
    """

    speed_profile = [target_speed/3.6] * len(cx)
    direction = 1.0  # forward

    speed_profile[-1] = 0.0

    return speed_profile


def read_global_path():
    global_path_x = []
    global_path_y = []
    # with open("/home/gigacha/Downloads/A2_LINK_432.json", 'r') as json_file:
    with open("/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/kcity_simul/semi_map.json", 'r') as json_file:
        json_data = json.load(json_file)
        for n, (x, y, mission, speed) in enumerate(json_data.values()):
            global_path_x.append(x)
            global_path_y.append(y)
    return global_path_x, global_path_y

################################################################
def mpc_pure_pursuit(node, ego_ind, global_path_x, global_path_y):
    i = 0 # v*dt = 거리 >> 내 x + 거리 = > 인덱스 찾아서 그 때의 스티어를 구하자
    steer_list = []
    for i in range(P.T + 1):
        i += 30
        target_index = ego_ind + i #self.ego_info.x'''''' + 49

        target_x, target_y = global_path_x[target_index], global_path_y[target_index]
        tmp = np.degrees(math.atan2(target_y - node.y,
                            target_x - node.x)) % 360

        alpha = node.yaw - tmp
        angle = math.atan2(2.0 * P.WB * math.sin(np.radians(alpha)), 1.0)
        angle = np.degrees(angle)
        if angle < 0.5 and angle > -0.5:
            angle = 0
        
        if abs(angle) > 5: 
            angle *= 0.7

        steer_list.append((max(min(angle, 27.0), -27.0))/3)
        
    return steer_list

def mpc_predict_next_state(z_ref, x0, y0, yaw0, v0, v_pre, steer_list):

    future_list = z_ref * 0.0

    future_list[0, 0] = x0
    future_list[1, 0] = y0
    future_list[2, 0] = yaw0
    future_list[3, 0] = v0
    # a_list = []

    v_pre = None

    for i in range(P.T):
        x1 = x0 + v0 * math.cos(yaw0) * P.dt 
        y1 = y0 + v0 * math.sin(yaw0) * P.dt
        yaw1 = yaw0 + v0 / P.WB * math.tan(steer_list[i]) * P.dt
        direct = 1
        
        if v_pre == None:
            # v_pre = v0
            a = 10
            v1 = v0 + direct * a * P.dt
        else:
            a = (v0 - v_pre)/P.dt
            v1 = v0 + direct * a * P.dt
        
        future_list[0, i+1] = x1
        future_list[1, i+1] = y1
        future_list[2, i+1] = yaw1
        future_list[3, i+1] = v1
        # a_list.append(a)

        x0 = x1
        y0 = y1
        yaw0 = yaw1
        v_pre = v0
        v0 = v1

    # return future_list, a_list
    return future_list

def mpc_cost_function_LJY(z_ref, z_bar, steer_list):
    i = 1
    cost = []
    for i in range(len(z_ref)):
        cost_function_1 = (z_ref[0][i] - z_bar[0][i])**2
        cost_function_2 = (z_ref[1][i] - z_bar[1][i])**2
        cost_function_3 = (z_ref[2][i] - z_bar[2][i])**2
        cost_function_4 = (z_ref[3][i] - z_bar[3][i])**2
        cost_function = cost_function_1 + cost_function_2 + cost_function_3 + cost_function_4
        cost.append(cost_function)

    selected_index = int(np.argmin(cost))
    return selected_index



################################################################

