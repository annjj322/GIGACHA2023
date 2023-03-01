import threading
import rospy
from shared.shared import Shared
from planner.planner import Planner
from localizer.localizer import Localizer
from controller.controller import Controller
from utils.sig_int_handler import ActivateSignalInterruptHandler
from utils.env_visualizer import Visualizer

from time import sleep

class Master(threading.Thread):
    def __init__(self, ui_rate):
        super().__init__()
        self.period = 1.0 / ui_rate

        rospy.init_node('master', anonymous=False)

    def run(self):
        self.shared = Shared()

        self.localizer = Localizer(self, rate=50)
        self.init_thread(self.localizer)

        self.planner = Planner(self, rate=20)
        self.init_thread(self.planner)

        self.controller = Controller(self, rate=20)
        self.init_thread(self.controller)

        self.visualizer = Visualizer(self, rate=10)
        self.init_thread(self.visualizer)

        while True:
            # rospy.loginfo("==========================")
            #rospy.loginfo("target_x : ", self.shared.perception.objx, "target_y : ", self.shared.perception.objy)
            # rospy.loginfo("state : {}".format(self.shared.state))
            rospy.loginfo("steer : {}".format(round(self.shared.ego.input_steer, 1)))
            rospy.loginfo("brake : {}".format(self.shared.ego.input_brake))
            rospy.loginfo("input_speed : {}".format(self.shared.ego.input_speed))
            rospy.loginfo("current_speed : {}".format(int(self.shared.ego.speed)))
            #rospy.loginfo("blue : {}".format(self.shared.ego.input_steer))

            sleep(self.period)

    def init_thread(self, module):
        module.daemon = True
        module.start()

    def checker_all(self):
        self.thread_checker(self.localizer)
        self.thread_checker(self.planner)
        self.thread_checker(self.controller)
        self.thread_checker(self.visualizer)

    def thread_checker(self, module):
        if not module.is_alive():
            print(type(module).__name__, "is dead..")

if __name__ == "__main__":
    ActivateSignalInterruptHandler()
    master = Master(ui_rate=10)
    master.start()