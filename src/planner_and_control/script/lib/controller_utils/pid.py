class PID:
    
    def __init__(self, eg):
        self.ego = eg
        self.pre_auto_manual = -1
        self.P = 0
        self.I = 0
        self.D = 0
        self.pre_error = 0.0
        self.error_sum = 0.0
        self.dt = 1.0 / 10.0
        self.target_ex = 0
        self.delta_target = 0

    def pid(self):
        if self.ego.auto_manual > self.pre_auto_manual : 
            self.error_sum = 0.0
            
            print("----------------------------------------")
        
        self.pre_auto_manual = self.ego.auto_manual
        print(self.error_sum)

        error = self.ego.target_speed - self.ego.speed
        diff_error = min(60, error - self.pre_error) 
        self.pre_error = error
        self.error_sum += error
        self.delta_target = abs(target - self.target_ex)

        self.speed = max(self.ego.target_speed - 1 , self.P*error + self.D*diff_error/self.dt + self.I*self.error_sum*self.dt)

    def decel(self):
        self.P = 1
        self.I = 1
        self.D = 1
        self.pid()

        return self.speed

    def accel(self):
        self.P = 5
        self.I = 0.5
        self.D = 1
        self.pid()

        return self.speed