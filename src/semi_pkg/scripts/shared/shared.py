from .ego import Ego
from .perception import Perception_
from .path import Path
from .plan import Plan
from .parking import Parking


class Shared:
    def __init__(self):
        # in common
        self.ego = Ego()

        # for perception
        self.perception = Perception_()

        # for planner
        self.global_path = Path()
        self.local_path=Path()
        self.plan = Plan()

        # for parking
        self.park = Parking()
        
        # potential field
        self.obstacles = []
     