from .path import Path

class Parking():
    def __init__(self):
        self.on = "off"
        self.mindex = 0
        self.forward_path = Path()
        self.backward_path = Path()
        self.direction = 0
        self.index = 0
        self.stop_index = 0
        self.select_num = 0
        self.o1x = 0
        self.o1y = 0
        self.o2x = 0
        self.o2y = 0
        self.o3x = 0
        self.o3y = 0
        self.inflection_point = 0
        self.inflection_on = False
