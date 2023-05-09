
import math as m
import numpy as np
from . import MPC

class LatController():
    def __init__(self, eg, sh, lattice, pl, park):
        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = park
        self.lattice_path = lattice

        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        # self.lookahead_default = 4 #look-ahead default

        self.path = self.lattice_path[self.shared.selected_lane]

        # cubic spline
        # self.cx, self.cy, self.cyaw, self.ck, self.s = MPC.cs.calc_spline_course(self.path.x, self.path.y, ds = MPC.P.d_dist)
        self.cx, self.cy, self.cyaw, self.ck, self.s = MPC.cs.calc_spline_course(self.global_path.x, self.global_path.y, ds = MPC.P.d_dist)

        # MPC initial
        self.sp = MPC.calc_speed_profile(self.cx, self.cy, self.cyaw, MPC.P.target_speed) # speed profile
        
        self.ref_path = MPC.PATH(self.cx, self.cy, self.cyaw, self.ck)
        
        self.node = MPC.Node(x=self.cx[0], y=self.cy[0], yaw=self.cyaw[0], v=0.0)

        self.time = 0.0
        self.x = [self.node.x]
        self.y = [self.node.y]
        self.yaw = [self.node.yaw]
        self.v = [self.node.v]
        self.t = []
        

    def run(self):
        while True:
            try:
                if self.parking.on == "on":
                    self.parking_run()
                elif self.parking.on == "forced":
                    self.parking_run2()
                elif self.parking.on == "U_turn":
                    self.U_turn()
                elif self.parking.on == "off":
                    self.Model_Predictive_Control()

                return self.steer

            except IndexError:
                print("++++++++lat_controller+++++++++")

    # def parking_run(self):
    #     if self.parking.direction == 0:
    #         self.path = self.parking.forward_path
    #         lookahead = 5
    #     else:
    #         self.path = self.parking.backward_path
    #         lookahead = 5
    #     # if not self.parking.inflection_on:
    #     target_index = lookahead + self.parking.index
    #     # else:
    #     #     target_index = len(self.parking.backward_path.x) - 1

    #     target_x, target_y = self.path.x[target_index], self.path.y[target_index]
    #     tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

    #     heading = self.ego.heading
    #     ###### Back Driving ######
    #     if self.ego.target_gear == 2:
    #         heading += 180
    #         heading %= 360
    #     ##########################

    #     alpha = heading - tmp
    #     angle = atan2(2.0 * self.WB *
    #                   sin(radians(alpha)) / lookahead, 1.0)

    #     ###### Back Driving ######
    #     if self.ego.target_gear == 2:
    #         angle = -1.5*angle
    #     ##########################

    #     if degrees(angle) < 3.5 and degrees(angle) > -3.5:
    #         angle = 0

    #     self.steer = max(min(degrees(angle), 27.0), -27.0)

    # def parking_run2(self):
    #     self.steer = self.ego.target_steer

    # def Pure_pursuit(self): # look ahead -> lattice 상의 cut_path에서 정하는 것으로
    #     self.path = self.lattice_path[self.shared.selected_lane]
    #     # print(len(self.lattice_path), "\n", self.shared.selected_lane)
    #     # self.path = self.shared.global_path
    #     lookahead = min(self.k * self.ego.speed +
    #                     self.lookahead_default, 6)
    #     target_index = len(self.path.x) - 49
    #     R2=sqrt(lookahead)/(2*abs(self.ego.x-self.path.x[target_index]))#퓨어퍼싯 기준 곡률반경계산 1이 넘을경우 곡선?
        
    #     # print(target_index)

    #     # lookahead = min(self.k * self.ego.speed + self.lookahead_default, 7)
    #     # target_index = int(lookahead * 10)

    #     target_x, target_y = self.path.x[target_index], self.path.y[target_index]
    #     tmp = degrees(atan2(target_y - self.ego.y,
    #                         target_x - self.ego.x)) % 360


    #     alpha = self.ego.heading - tmp
    #     angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)
    #     if degrees(angle) < 0.5 and degrees(angle) > -0.5:
    #         angle = 0
    #     tmp_steer = degrees(angle) # * 1.1 후진시에 의도적인 over steer
    #     if abs(tmp_steer) > 5: # [degree] 곡선 부드럽게 하는 코드
    #         tmp_steer *= 0.8

    #     self.steer = max(min(tmp_steer, 27.0), -27.0) 
    #     return self.steer
    
    # def normailizer(self):

    
    def Model_Predictive_Control(self):
        self.node.x = self.ego.x
        self.node.y = self.ego.y
        self.node.yaw = self.ego.heading
        self.node.v = self.ego.speed

        ego_ind = self.nearest_index(self.node)
        
        print("path.x: ",len(self.path.x))
        print("globalpath.x: ",len(self.global_path.x))
        print("path.y: ",len(self.path.y))
        print("globalpath.y: ",len(self.global_path.y))

        self.x.append(self.node.x)
        self.y.append(self.node.y)
        self.yaw.append(self.node.yaw)
        self.v.append(self.node.v)
        
        z_ref = MPC.calc_ref_trajectory_in_T_step(self.node, ego_ind, self.ref_path, self.sp) # 내 인덱스에서 미래 reference state
        steer_list = MPC.mpc_pure_pursuit(self.node, ego_ind, self.cx, self.cy) # 내 위치에서 뽑아낸 미래 예측 steer들
        z_bar = MPC.mpc_predict_next_state(z_ref, self.node.x, self.node.y, self.node.yaw, self.node.v, self.v[-1], steer_list) # 미래 예측된 state # 위에서 뽑은 걸 기반으로 뽑아낸 예측 state
        selected_index = MPC.mpc_cost_function_LJY(z_ref, z_bar, steer_list) # z_ref와 z_bar을 기반으로 해서 다음 state index 정하기
        self.steer = steer_list[selected_index]
        # print(ego_ind)
        # print(selected_index)
        # print(self.steer)
        # print(self.parking.on)
        return self.steer

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