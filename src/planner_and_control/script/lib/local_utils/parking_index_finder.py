from math import hypot
from planner_and_control.msg import Ego
from lib.general_utils.read_global_path import read_global_path
from planner_and_control.msg import Path

class ParkingIndexFinder:
    def __init__(self, eg, path):
        self.ego = Ego()
        self.ego = eg
        self.index = 0
        self.path = path

    def run(self):
        min_dis = -1
        min_idx = 0
        step_size = 10
        save_idx = 0

        for i in range(max(self.index - step_size, 0), self.index + step_size):
            try:
                dis = hypot(self.path.x[i] - self.ego.x, self.path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i

        self.index = min_idx
        return self.index