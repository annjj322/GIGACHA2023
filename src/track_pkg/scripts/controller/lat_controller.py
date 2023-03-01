from math import hypot, cos, sin, degrees, atan2, radians, pi

class LatController():
    def __init__(self, sh, eg):
 
        self.shared = sh
        self.ego = eg

        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):
        while True:
            try:
                if self.ego.percep_state == "y_turn":
                    self.forced_angle1()
                elif self.ego.percep_state == "b_turn":
                    self.forced_angle2()
                else:
                    target_x, target_y = self.ego.point_x, self.ego.point_y
                    tmp = degrees(atan2(target_y, target_x)) % 360
                    distance = hypot(target_x, target_y)
                    alpha = -tmp
                    angle = atan2(2.0 * self.WB * sin(radians(alpha)) / distance, 1.0)

                    if degrees(angle) < 1 and degrees(angle) > -1:
                        angle = 0

                    self.steer = max(min(degrees(angle), 27.0), -27.0)
                
                return self.steer

            except ZeroDivisionError:
                print("+++++++++lat_control++++++++")

    def forced_angle1(self):
        self.steer = 23

    def forced_angle2(self):
        self.steer = -23      