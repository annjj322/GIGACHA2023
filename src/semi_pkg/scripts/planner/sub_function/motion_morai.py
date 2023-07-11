from math import sqrt
from math import sqrt
from math import cos,sin,atan2
import numpy as np
from shared.path import Path

class Motion():
    def __init__(self, sh, pl, eg):
        self.shared = sh
        self.plan = pl
        self.ego = eg

        self.global_path = self.shared.global_path # from localizer
        