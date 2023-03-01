import threading
import rospy
from time import sleep
from .lat_controller import LatController
# from .lon_controller import LonController
from local_pkg.msg import Control_Info

class Controller(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego
        self.plan = parent.shared.plan
        self.parking = parent.shared.park
        self.lattice_path = parent.shared.lattice_path

        self.serial_pub = rospy.Publisher("controller", Control_Info, queue_size=1)        

        self.lat_controller = LatController(self.ego, self.shared, self.lattice_path, self.plan, self.parking)
        # self.lon_controller = LonController(self.ego, self.shared)

    def run(self):
        while True:
            try:
                self.ego.input_steer = self.lat_controller.run()
                # self.ego.input_speed = self.lon_controller.run()
                if self.plan.behavior_decision == "driving":
                    self.ego.input_speed = self.ego.map_speed[self.ego.index]
                else:
                    self.ego.input_speed = self.ego.target_speed
                self.ego.input_brake = self.ego.target_brake
                self.ego.input_gear = self.ego.target_gear
                

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