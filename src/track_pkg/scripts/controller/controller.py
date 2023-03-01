import threading
import rospy
from time import sleep
from .lat_controller import LatController
from .lon_controller import LonController
from local_pkg.msg import Control_Info

class Controller(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego

        self.serial_pub = rospy.Publisher("controller", Control_Info, queue_size=1)        

        self.lat_controller = LatController(self.shared, self.ego)
        self.lon_controller = LonController(self.ego, self.shared)

    def run(self):
        while True:
            try:
                self.ego.input_steer = self.lat_controller.run()
                self.ego.input_speed, self.ego.input_brake = self.lon_controller.run()
                # self.ego.input_brake = self.ego.target_brake
                # self.ego.input_gear = self.ego.target_gear

                # print("speed : ", self.ego.input_speed)
                ######################## SERIAL ################################
                serial = Control_Info()
                serial.emergency_stop = self.ego.input_estop
                serial.gear = self.ego.input_gear
                serial.speed = self.ego.input_speed
                serial.steer = self.ego.input_steer
                serial.brake = self.ego.input_brake

                self.serial_pub.publish(serial)

            except IndexError:
                print("+++++++controller++++++")

            sleep(self.period)