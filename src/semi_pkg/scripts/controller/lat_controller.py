from math import sin, degrees, atan2, radians, cos
from numpy import clip
from time import sleep
class LatController():
    def __init__(self, eg, sh, pl, park):
        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = park
        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        self.lookahead = 3
        self.target_index = self.ego.index+self.lookahead
   
    def run(self):
        while True:
            try:
                return self.Pure_pursuit()
            except IndexError:
                # sleep(1)
                print("++++++++lat_controller+++++++++")

    def Pure_pursuit(self, lookahead=None):
        heading = self.ego.heading
        x = self.ego.x
        y = self.ego.y

        self.path = self.shared.global_path

        # self.lookahead decision  
        if lookahead == None:  
            if self.ego.target_gear == 2:
                self.lookahead = int(clip((9*self.ego.target_speed-120), 18, 60))
            else:
                self.lookahead = int(clip((9*self.ego.target_speed-120), 24, 60))
        else:
            self.lookahead = lookahead

        self.target_index = self.ego.index + min(self.lookahead, len(self.path.x)-1)
        if self.target_index >= len(self.global_path.x)-1:
            self.target_index = len(self.global_path.x)-1
            
        target_x, target_y = self.path.x[self.target_index], self.path.y[self.target_index]
        tmp = degrees(atan2(target_y - y, target_x - x)) % 360
        alpha = tmp - heading
        angle = atan2(2.0 * self.WB * sin(radians(alpha)), self.lookahead/6)
        tmp_steer = degrees(angle) 
        
        self.steer = float(clip(-tmp_steer, -27.0, 27.0))

        return self.steer