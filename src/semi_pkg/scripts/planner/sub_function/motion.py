from math import sqrt
from math import sqrt
from math import cos,sin,atan2,atan
import numpy as np
from shared.path import Path
import threading
class Motion():
    def __init__(self, sh, pl, eg):
        self.L = 1.5
        self.shared = sh
        self.plan = pl
        self.ego = eg
        self.lane_lock=threading.Lock()

        self.global_path = self.shared.global_path # from localizer