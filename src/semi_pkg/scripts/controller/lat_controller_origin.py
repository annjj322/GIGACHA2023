from math import sin, degrees, atan2, radians
from numpy import rad2deg
class LatController():
    def __init__(self, eg, sh, lattice, pl, park):
        """
        """
 
        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = park
        self.lattice_path = lattice 

        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):
        while True:
            try:
                if self.parking.on == "on":
                    # self.parking_run()
                    self.parking_run_LJY()
                elif self.parking.on == "forced":
                    self.parking_run2()
                elif self.parking.on == "U_turn":
                    self.U_turn()
                elif self.parking.on == "off":
                    self.Pure_pursuit()

                # return self.steer
                return self.Pure_pursuit()
            except IndexError:
                print("++++++++lat_controller+++++++++")

    def parking_run(self):
        if self.parking.direction == 0:
            self.path = self.parking.forward_path
            lookahead = 5
        else:
            self.path = self.parking.backward_path
            lookahead = 5
        # if not self.parking.inflection_on:
        # target_index = lookahead + len(self.parking.backward_path.x)
        # else:
        #     target_index = len(self.parking.backward_path.x) - 1

        target_x, target_y = self.path.x[-1], self.path.y[-1]
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

        heading = self.ego.heading
        ###### Back Driving ######
        if self.ego.target_gear == 2:
            heading += 180
            heading %= 360
        ##########################

        alpha = heading - tmp
        angle = atan2(2.0 * self.WB *
                      sin(radians(alpha)) / lookahead, 1.0)

        ###### Back Driving ######
        if self.ego.target_gear == 2:
            angle = -1.5*angle
        ##########################

        if degrees(angle) < 3.5 and degrees(angle) > -3.5:
            angle = 0

        self.steer = max(min(degrees(angle), 27.0), -27.0)

    def parking_run2(self):
        self.steer = self.ego.target_steer

    def Pure_pursuit(self):
        self.path = self.lattice_path[self.shared.selected_lane]
        # print(len(self.lattice_path), "\n", self.shared.selected_lane)
        # self.path = self.shared.global_path
        # if self.ego.heading==rad2deg(2.6623):
        #     self.target_gear=1
        # else:
        #     self.target_gear=2
        lookahead = min(self.k * self.ego.speed +
                        self.lookahead_default, 6)
        target_index =len(self.path.x) - 49
        # print(target_index)

        # lookahead = min(self.k * self.ego.speed + self.lookahead_default, 7)
        # target_index = int(lookahead * 10)

        target_x, target_y = self.path.x[target_index], self.path.y[target_index]
        tmp = degrees(atan2(target_y - self.ego.y,
                            target_x - self.ego.x)) % 360
        

        alpha = self.ego.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)
        if degrees(angle) < 0.5 and degrees(angle) > -0.5:
            angle = 0
        tmp_steer = degrees(angle)
        if abs(tmp_steer) > 5: # [degree] 곡선 부드럽게 하는 코드
            tmp_steer *= 0.8

        self.steer = max(min(tmp_steer, 27.0), -27.0)
        return self.steer

    def parking_run_LJY(self):
        # if self.parking.direction == 0:
        #     self.global_path = self.parking.forward_path
        #     lookahead = 5
        # else:
        #     self.global_path = self.parking.backward_path
        lookahead = 2

        target_x, target_y = self.global_path.x[self.ego.index + lookahead], self.global_path.y[self.ego.index + lookahead]
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

        heading = self.ego.heading
        ###### Back Driving ######
        if self.ego.target_gear == 2:
            heading += 180
            heading %= 360
        ##########################

        alpha = heading - tmp
        angle = atan2(2.0 * self.WB *
                      sin(radians(alpha)) / lookahead, 1.0)

        # ###### Back Driving ######
        # if self.ego.target_gear == 2:
        #     angle = -1.5*angle
        # ##########################

        if degrees(angle) < 3.5 and degrees(angle) > -3.5:
            angle = 0

        self.steer = max(min(degrees(angle), 27.0), -27.0)

        return self.steer
