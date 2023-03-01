from geometry_msgs.msg import Quaternion

class Ego():
    def __init__(self):
        # Local to Ego
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.index = int(0)
        self.orientation = Quaternion()
        self.map_speed = []
        
        # Odometry
        self.dr_x = 0
        self.dr_y = 0
        self.dis = 0.0

        # Serial to Ego (reader)
        self.auto_manual = 0
        self.emergency_stop = 0
        self.encoder = []
        self.speed = 0
        self.brake = 0
        self.gear = 0
        self.steer = 0
        self.alive = 0

        # Planner to Controller
        self.target_estop = 0x00
        self.target_speed = 10
        self.target_gear = 0
        self.target_brake = 0
        self.target_estop = 0
        self.target_steer = 0

        # Controller to Serial (writer)
        self.input_estop = 0x00
        self.input_gear = 0
        self.input_speed = 10
        self.input_steer = 0
        self.input_brake = 0
