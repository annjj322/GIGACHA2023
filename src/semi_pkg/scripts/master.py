import threading
import rospy
import argparse
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

    def run(self):
        self.shared = Shared()

        self.localizer = Localizer(self, rate=10)
        self.init_thread(self.localizer)

        self.mission_planner = MissionPlanner(self, rate=10)
        self.init_thread(self.mission_planner)

        self.behavior_planner = BehaviorPlanner(self, rate=10)
        self.init_thread(self.behavior_planner)

        self.motion_planner = MotionPlanner(self, rate=10)
        self.init_thread(self.motion_planner)

        self.controller = Controller(self, rate=10)
        self.init_thread(self.controller)

        self.visualizer = Visualizer(self, rate=10)
        self.init_thread(self.visualizer)

        while True:
            print('------------------------------------- \
                  \nBehavior_decision : {} | Input speed : {} \
                  \nTarget speed : {:.2f} | Steer : {:.2f} \
                  \n Target index : {} | Lookahead : {} \
                  \nIndex : {} | Local index : {} \
                  \nx : {:.2f} | y : {:.2f} | Heading : {:.2f} \
                  '.format(
                    self.shared.plan.behavior_decision, 
                    self.shared.ego.input_speed,
                    self.shared.ego.target_speed, 
                    self.shared.ego.input_steer, 
                    self.controller.lat_controller.target_index,
                    self.controller.lat_controller.lookahead,
                    self.shared.ego.index,
                    self.shared.ego.local_index,
                    self.shared.ego.x,
                    self.shared.ego.y,
                    self.shared.ego.heading
                    ))
            
            self.checker_all()

            sleep(self.period)

    def init_thread(self, module):
        module.daemon = True # daemon 쓰레드로 설정
        module.start() # module.run() 실행

    def checker_all(self):
        self.thread_checker(self.localizer)
        self.thread_checker(self.mission_planner)    
        self.thread_checker(self.behavior_planner)
        self.thread_checker(self.motion_planner)
        self.thread_checker(self.controller)
        self.thread_checker(self.visualizer)

    def thread_checker(self, module):
        if not module.is_alive():
            print(type(module).__name__, "is dead..")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="GIGACHA"
    )
    argparser.add_argument(
        '--map',
        
        # default='kcity_simul/semi_map', #go
        # default='kcity_simul/semi_map_parrallel_parking', # parrallel parking
        # default='kcity_simul/semi_map_diagonal_parking', # diagonal parking
        # default='kcity_simul/semi_map_delivery', # delivery
        default='kcity_simul/semi_map_obs_tmp',
        # default='kcity_simul/semi_map_driving',
        # default='kcity_simul/parallelpark_map', # parking2
        help='kcity/map1, songdo/map2, yonghyeon/Yonghyeon, kcity_simul/left_lane, kcity_simul/right_lane, kcity_simul/final, inha_parking/gpp, kcity_simul/semi_map, kcity_simul/parallelpark'
    )

    ActivateSignalInterruptHandler()
    args = argparser.parse_args()
    master = Master(args, ui_rate=10)
    master.start()
