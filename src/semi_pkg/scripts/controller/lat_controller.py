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
                if self.global_path.mission[self.ego.index] == "obs_tmp":
                    return self.pure_pursuit()
                    
                else:
                    return self.pure_pursuit()
            except IndexError:
                # sleep(1)
                # print("++++++++lat_controller+++++++++")
                pass

    def pure_pursuit(self, lookahead=None):
        heading = self.ego.heading
        x = self.ego.x
        y = self.ego.y
        
        self.path = self.shared.global_path
        
        # self.lookahead decision  
        if lookahead == None:  
            if self.ego.target_gear == 2:
                self.lookahead = int(clip((9*self.ego.target_speed-120), 18, 60))
            else:
                self.lookahead = int(clip((9*self.ego.target_speed-120), 30, 60))
        else:
            self.lookahead = lookahead

        self.target_index = self.ego.index + min(self.lookahead, len(self.path.x)-1)
        if self.target_index >= len(self.path.x)-1:
            self.target_index = len(self.path.x)-1
            
        target_x, target_y = self.path.x[self.target_index], self.path.y[self.target_index]
        tmp = degrees(atan2(target_y - y, target_x - x)) % 360
        alpha = tmp - heading
        angle = atan2(2.0 * self.WB * sin(radians(alpha)), self.lookahead/6)
        tmp_steer = degrees(angle) 
        
        self.steer = float(clip(-tmp_steer, -27.0, 27.0))

        return self.steer
    
    def local_pure_pursuit(self, lookahead=None):
        heading = self.ego.heading
        x = self.ego.x
        y = self.ego.y
        
        self.path = self.shared.local_path

        # self.lookahead decision  
        # self.lookahead = 30
        self.lookahead = len(self.path.x)-1

        self.target_index = self.lookahead
        
        # if self.target_index >= len(self.path.x)-1:
        #     self.target_index = len(self.path.x)-1
  
        target_x, target_y = self.path.x[self.target_index], self.path.y[self.target_index]
        tmp = degrees(atan2(target_y - y, target_x - x)) % 360
        alpha = tmp - heading
        angle = atan2(2.0 * self.WB * sin(radians(alpha)), self.lookahead/6)
        tmp_steer = degrees(angle) 
        
        self.steer = float(clip(-tmp_steer, -27.0, 27.0)) * 3

        return self.steer