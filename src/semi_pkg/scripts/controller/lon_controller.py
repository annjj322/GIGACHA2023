class LonController():
    def __init__(self, eg, sh):
        self.ego = eg
        self.shared = sh

    def run(self): 
        return self.ego.target_speed
