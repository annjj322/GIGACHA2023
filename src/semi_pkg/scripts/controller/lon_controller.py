import numpy as np
from math import sqrt
from time import sleep
import matplotlib.pyplot as plt
class LonController():
    def __init__(self, eg, sh, pl, pk):
        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = pk
        self.speed = 0

    def run(self, speed = None):
        if self.parking.on == "on":
            self.speed = self.ego.target_speed
            print("1111111111111111")
        else:
            print(222222222222)
            if speed == None:
                self.speed = np.round(self.shared.ego.map_speed[self.ego.index], 2)
            else:
                self.speed = speed

        return self.speed
           
        
        