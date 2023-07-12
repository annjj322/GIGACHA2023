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
        self.plan = parent.shared.plan
        self.parking = parent.shared.park

        self.serial_pub = rospy.Publisher("controller", Control_Info, queue_size=1)        

        self.lat_controller = LatController(self.ego, self.shared, self.plan, self.parking)
        self.lon_controller = LonController(self.ego, self.shared, self.plan, self.parking)

        self.control_lock = threading.Lock()

    def run(self):
        while True:
            try:
                self.control_lock.acquire()
                # Value decision
                self.ego.input_gear = self.ego.target_gear
                self.ego.input_brake = self.ego.target_brake
                self.ego.input_speed = self.lon_controller.run()
                if self.parking.on =='on':
                    self.ego.input_steer = self.ego.target_steer
                else:
                    self.ego.input_steer = self.lat_controller.run() 
               
                # To serial 
                serial = Control_Info()
                serial.emergency_stop = self.ego.input_estop
                serial.gear = self.ego.input_gear
                serial.speed = self.ego.input_speed
                serial.steer = self.ego.input_steer
                serial.brake = self.ego.input_brake

                self.serial_pub.publish(serial) 
                self.control_lock.release()

            except IndexError:
                print("+++++++controller++++++")

            sleep(self.period)