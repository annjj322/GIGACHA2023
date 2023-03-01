from math import hypot, cos, sin, degrees, atan2, radians, pi, sqrt
import numpy as np

class Stanley:
    def __init__(self, eg, trajectory, parking):



        self.ego = eg
        self.yaw = []
        self.parking = parking
        self.WB = 1.04  # wheel base
        self.k = -0.8  # CTR parameter
        self.path = trajectory
        self.index = 0
        self.cnt = 0

    def normalize(self, angle):
        while angle > pi:
            angle -= 2.0 * pi

        while angle < -pi:
            angle += 2.0 * pi

        return angle

    def make_yaw(self):
        # for i in range(len(self.path.x)-1):
        #     self.yaw.append(atan2(self.path.y[i+1]-self.path.y[i],
        #                           self.path.x[i+1]-self.path.x[i]))
        for i in range(len(self.path.data.x)-1):
            self.yaw.append(atan2(self.path.data.y[i+1]-self.path.data.y[i],
                                  self.path.data.x[i+1]-self.path.data.x[i]))

    def run(self):
        if self.parking.on == True:
            self.index = self.parking.index
            if len(self.yaw) != 0 and self.cnt == 0:
                self.yaw = []
                self.cnt = 1
        else:
            # self.index = self.ego.index
            self.index = self.ego.data.index

        if len(self.yaw) == 0:
            self.make_yaw()

        # front_x = self.ego.x + 0.5*self.WB*cos(radians(self.ego.heading))
        # front_y = self.ego.y + 0.5*self.WB*sin(radians(self.ego.heading))
        front_x = self.ego.data.x + 0.5*self.WB*cos(radians(self.ego.data.heading))
        front_y = self.ego.data.y + 0.5*self.WB*sin(radians(self.ego.data.heading))

        # map_x, map_y = self.path.x[self.index], self.path.y[self.index]
        # print("self index : ", self.index)
        # print(self.path.data.x)
        # print(self.path.data.y)
        map_x, map_y = self.path.data.x[self.index], self.path.data.y[self.index]
        map_yaw = self.yaw[self.index]
        dx = map_x - front_x
        dy = map_y - front_y

        # perp_vec = [cos(radians(self.ego.heading)+pi/2),
        #             sin(radians(self.ego.heading)+pi/2)]
        perp_vec = [cos(radians(self.ego.data.heading)+pi/2),
                    sin(radians(self.ego.data.heading)+pi/2)]
        cte = np.dot([dx, dy], perp_vec)

        # if self.ego.mode != "driving":
        #     k_s = 4.0 # must change
        # else :
        #     k_s = 0
        k_s = 0

        # final_yaw = -(map_yaw - radians(self.ego.heading))
        final_yaw = -(map_yaw - radians(self.ego.data.heading))

        yaw_term = self.normalize(final_yaw)
        # cte_term = atan2(self.k*cte, self.ego.speed + k_s)
        cte_term = atan2(self.k*cte, self.ego.data.speed + k_s)

        steer = degrees(yaw_term + cte_term)

        # print(f"self.ego.heading : {self.ego.heading}")
        print(f"self.ego.heading : {self.ego.data.heading}")
        print(f"yaw_term : {degrees(yaw_term)}")
        print(f"cte_term : {degrees(cte_term)}")
        print(f"-----index : {self.index}")

        return max(min(steer, 27.0), -27.0)
