import threading
import rospy
import argparse
# from local_pkg.msg import Guii
from shared.shared import Shared
from localizer.localizer import Localizer
from planner.mission_planner import MissionPlanner
from planner.behavior_planner import BehaviorPlanner
from planner.motion_planner import MotionPlanner
from controller.controller import Controller
from utils.sig_int_handler import ActivateSignalInterruptHandler
from utils.env_visualizer import Visualizer

from time import sleep

class Master(threading.Thread):
    def __init__(self, args, ui_rate):
        super().__init__()
        self.args = args
        self.period = 1.0 / ui_rate

        rospy.init_node('master', anonymous=False)

        self.dead_index = 0

    def run(self):
        self.shared = Shared()

        self.localizer = Localizer(self, rate=50)
        self.init_thread(self.localizer)

        self.mission_planner = MissionPlanner(self, rate=10)
        self.init_thread(self.mission_planner)

        self.behavior_planner = BehaviorPlanner(self, rate=10)
        self.init_thread(self.behavior_planner)

        self.motion_planner = MotionPlanner(self, rate=20)
        self.init_thread(self.motion_planner)

        self.controller = Controller(self, rate=20)
        self.init_thread(self.controller)

        self.visualizer = Visualizer(self, rate=10)
        self.init_thread(self.visualizer)

        while True:
            # print("---------------------")

            # print('x : {0:.2f}, y : {1:.2f}, index : {2}, \nheading : {3:.2f}'\
            #     .format(self.shared.ego.x, self.shared.ego.y, self.shared.ego.index, self.shared.ego.heading))
            print('index :', self.shared.ego.index)
            print('heading :', self.shared.ego.heading)
            print('Mission_State : {}'.format(self.shared.plan.state))
            print('Behavior_Decision : {}'.format(self.shared.plan.behavior_decision))
            # print('speed : ', self.shared.ego.input_speed)
            # print("red : ", self.shared.perception.tred, ", yellow : ", self.shared.perception.tyellow, ", green : ", self.shared.perception.tgreen, ", left : ", self.shared.perception.tleft)
            # # # # print('Motion_Selected lane : {}'.format(self.shared.selected_lane))
            # print('Speed : {}, Steer : {:.2f}'.format(self.shared.ego.input_speed, self.shared.ego.input_steer))
            # print('Current Speed : {},'.format(self.shared.ego.speed))
            # print(self.shared.ego.dis)

            self.checker_all()

            sleep(self.period)

    def init_thread(self, module):
        module.daemon = True
        module.start()

    def checker_all(self):
        self.thread_checker(self.localizer)
        self.thread_checker(self.mission_planner)    
        self.thread_checker(self.behavior_planner)
        self.thread_checker(self.motion_planner)
        self.thread_checker(self.controller)
        self.thread_checker(self.visualizer)

    def thread_checker(self, module):
        if not module.is_alive():
            print(type(module).__name__, "is dead.. at : ", self.dead_index)
            if self.dead_index == 0:
                self.dead_index = self.shared.ego.index


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="GIGACHA"
    )
    argparser.add_argument(
        '--map',
        default='kcity_simul/final_map_jj',
        help='kcity_simul/final_map, Siheung/delivery2, Siheung/sibaedal'
    )

    ActivateSignalInterruptHandler()
    args = argparser.parse_args()
    master = Master(args, ui_rate=10)
    master.start()
