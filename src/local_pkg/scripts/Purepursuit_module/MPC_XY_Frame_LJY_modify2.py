"""
Linear MPC controller (X-Y frame)
author: huiming zhou
"""

import os
import sys
import math
import cvxpy
import numpy as np
import matplotlib.pyplot as plt
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import draw as draw
import reeds_shepp as rs
import cubic_spline as cs


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
    target_speed = 10.0 * 3.6  # target speed
    N_IND = 10  # search index number
    dt = 0.2  # time step
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
    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0, direct=1.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.direct = direct #방향 

    def update(self, a, delta, direct): #가속도랑 조향각, 방향
        delta = self.limit_input_delta(delta) #최대 조향각 조절
        self.x += self.v * math.cos(self.yaw) * P.dt 
        self.y += self.v * math.sin(self.yaw) * P.dt
        self.yaw += self.v / P.WB * math.tan(delta) * P.dt
        self.direct = direct
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

        dx = [node.x - x for x in self.cx[self.ind_old: (self.ind_old + P.N_IND)]]
        dy = [node.y - y for y in self.cy[self.ind_old: (self.ind_old + P.N_IND)]]
        dist = np.hypot(dx, dy)

        ind_in_N = int(np.argmin(dist))
        ind = self.ind_old + ind_in_N
        self.ind_old = ind

        rear_axle_vec_rot_90 = np.array([[math.cos(node.yaw + math.pi / 2.0)],
                                         [math.sin(node.yaw + math.pi / 2.0)]])

        vec_target_2_rear = np.array([[dx[ind_in_N]],
                                      [dy[ind_in_N]]])

        er = np.dot(vec_target_2_rear.T, rear_axle_vec_rot_90)
        er = er[0][0]

        return ind, er


def calc_ref_trajectory_in_T_step(node, ref_path, sp):
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

    ind, _ = ref_path.nearest_index(node)

    z_ref[0, 0] = ref_path.cx[ind]
    z_ref[1, 0] = ref_path.cy[ind]
    z_ref[2, 0] = ref_path.cyaw[ind]
    z_ref[3, 0] = sp[ind]

    dist_move = 0.0

    for i in range(1, P.T + 1):
        dist_move += abs(node.v) * P.dt
        ind_move = int(round(dist_move / P.d_dist))
        index = min(ind + ind_move, length - 1)

        z_ref[0, i] = ref_path.cx[index]
        z_ref[1, i] = ref_path.cy[index]
        z_ref[2, i] = ref_path.cyaw[index]
        z_ref[3, i] = sp[index]

    return z_ref, ind


def linear_mpc_control(z_ref, z0, a_old, delta_old):
    """
    linear mpc controller
    :param z_ref: reference trajectory in T steps
    :param z0: initial state vector
    :param a_old: acceleration of T steps of last time
    :param delta_old: delta of T steps of last time
    :return: acceleration and delta strategy based on current information
    """

    if a_old is None or delta_old is None:
        a_old = [0.0] * P.T
        delta_old = [0.0] * P.T

    x, y, yaw, v = None, None, None, None

    for k in range(P.iter_max):
        z_bar = predict_states_in_T_step(z0, a_old, delta_old, z_ref)
        a_rec, delta_rec = a_old[:], delta_old[:]
        a_old, delta_old, x, y, yaw, v = solve_linear_mpc(z_ref, z_bar, z0, delta_old)

        du_a_max = max([abs(ia - iao) for ia, iao in zip(a_old, a_rec)])
        du_d_max = max([abs(ide - ido) for ide, ido in zip(delta_old, delta_rec)])

        if max(du_a_max, du_d_max) < P.du_res:
            break

    return a_old, delta_old, x, y, yaw, v


def predict_states_in_T_step(z0, a, delta, z_ref):
    """
    given the current state, using the acceleration and delta strategy of last time,
    predict the states of vehicle in T steps.
    :param z0: initial state
    :param a: acceleration strategy of last time
    :param delta: delta strategy of last time
    :param z_ref: reference trajectory
    :return: predict states in T steps (z_bar, used for calc linear motion model)
    """

    z_bar = z_ref * 0.0

    for i in range(P.NX):
        z_bar[i, 0] = z0[i]

    node = Node(x=z0[0], y=z0[1], v=z0[2], yaw=z0[3])

    for ai, di, i in zip(a, delta, range(1, P.T + 1)):
        node.update(ai, di, 1.0)
        z_bar[0, i] = node.x
        z_bar[1, i] = node.y
        z_bar[2, i] = node.v
        z_bar[3, i] = node.yaw

    return z_bar


def calc_linear_discrete_model(v, phi, delta):
    """
    calc linear and discrete time dynamic model.
    :param v: speed: v_bar
    :param phi: angle of vehicle: phi_bar
    :param delta: steering angle: delta_bar
    :return: A, B, C
    """

    A = np.array([[1.0, 0.0, P.dt * math.cos(phi), - P.dt * v * math.sin(phi)],
                  [0.0, 1.0, P.dt * math.sin(phi), P.dt * v * math.cos(phi)],
                  [0.0, 0.0, 1.0, 0.0],
                  [0.0, 0.0, P.dt * math.tan(delta) / P.WB, 1.0]])

    B = np.array([[0.0, 0.0],
                  [0.0, 0.0],
                  [P.dt, 0.0],
                  [0.0, P.dt * v / (P.WB * math.cos(delta) ** 2)]])

    C = np.array([P.dt * v * math.sin(phi) * phi,
                  -P.dt * v * math.cos(phi) * phi,
                  0.0,
                  -P.dt * v * delta / (P.WB * math.cos(delta) ** 2)])

    return A, B, C


def solve_linear_mpc(z_ref, z_bar, z0, d_bar):
    """
    solve the quadratic optimization problem using cvxpy, solver: OSQP
    :param z_ref: reference trajectory (desired trajectory: [x, y, v, yaw])
    :param z_bar: predicted states in T steps
    :param z0: initial state
    :param d_bar: delta_bar
    :return: optimal acceleration and steering strategy
    """

    z = cvxpy.Variable((P.NX, P.T + 1))
    u = cvxpy.Variable((P.NU, P.T)) # T = 6

    cost = 0.0
    constrains = []

    for t in range(P.T):
        cost += cvxpy.quad_form(u[:, t], P.R)
        cost += cvxpy.quad_form(z_ref[:, t] - z[:, t], P.Q)

        A, B, C = calc_linear_discrete_model(z_bar[2, t], z_bar[3, t], d_bar[t])

        constrains += [z[:, t + 1] == A @ z[:, t] + B @ u[:, t] + C]

        if t < P.T - 1:
            cost += cvxpy.quad_form(u[:, t + 1] - u[:, t], P.Rd)
            constrains += [cvxpy.abs(u[1, t + 1] - u[1, t]) <= P.steer_change_max * P.dt]

    cost += cvxpy.quad_form(z_ref[:, P.T] - z[:, P.T], P.Qf)

    constrains += [z[:, 0] == z0]
    constrains += [z[2, :] <= P.speed_max]
    constrains += [z[2, :] >= P.speed_min]
    constrains += [cvxpy.abs(u[0, :]) <= P.acceleration_max]
    constrains += [cvxpy.abs(u[1, :]) <= P.steer_max]

    prob = cvxpy.Problem(cvxpy.Minimize(cost), constrains)
    prob.solve(solver=cvxpy.OSQP)

    a, delta, x, y, yaw, v = None, None, None, None, None, None

    if prob.status == cvxpy.OPTIMAL or \
            prob.status == cvxpy.OPTIMAL_INACCURATE:
        x = z.value[0, :]
        y = z.value[1, :]
        v = z.value[2, :]
        yaw = z.value[3, :]
        a = u.value[0, :]
        delta = u.value[1, :]
    else:
        print("Cannot solve linear mpc!")

    return a, delta, x, y, yaw, v


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

    # Set stop point
    # for i in range(len(cx) - 1):
    #     dx = cx[i + 1] - cx[i]
    #     dy = cy[i + 1] - cy[i]

    #     move_direction = math.atan2(dy, dx)

    #     if dx != 0.0 and dy != 0.0:
    #         dangle = abs(pi_2_pi(move_direction - cyaw[i]))
    #         if dangle >= math.pi / 4.0:
    #             direction = -1.0
    #         else:
    #             direction = 1.0

    #     if direction != 1.0:
    #         speed_profile[i] = - target_speed
    #     else:
    #         speed_profile[i] = target_speed

    speed_profile[-1] = 0.0

    return speed_profile


def pi_2_pi(angle):
    if angle > math.pi:
        return angle - 2.0 * math.pi

    if angle < -math.pi:
        return angle + 2.0 * math.pi

    return angle

def read_global_path():
    global_path_x = []
    global_path_y = []
    with open("/home/gigacha/Downloads/longtest.json", 'r') as json_file:
    # with open("/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/kcity_simul/semi_map.json", 'r') as json_file:
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
            angle *= 0.8

        steer_list.append((max(min(angle, 27.0), -27.0))/3)
        
    return steer_list

def mpc_predict_next_state(z_ref, x0, y0, yaw0, v0, v_pre, steer_list, direct = 1):

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
        direct = direct
        
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

