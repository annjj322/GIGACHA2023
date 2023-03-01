class LonController():
    def __init__(self, eg, sh):
        self.ego = eg
        self.shared = sh
        self.speed = 0
        self.brake = 0

    def run(self):
        if abs(self.ego.input_steer) > 15:
            if self.ego.speed > 7:
                self.brake = 20
                self.speed = 0
            else:
                self.brake = 0
                self.speed = 7

        elif abs(self.ego.input_steer) > 10:
            if self.ego.speed > 10:
                self.brake = 25
                self.speed = 0
            else:
                self.brake = 0
                self.speed = 10
        else:
            self.speed = 13

        return self.speed, self.brake