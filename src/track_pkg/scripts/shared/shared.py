from .ego import Ego
from .perception import Perception_
from .path import Path

class Shared:
    def __init__(self):
        # in common 
        self.ego = Ego()

        # for perception
        self.perception = Perception_()

        # for planner
        self.state = "1st"
        self.global_path = Path()