#!/usr/bin/env python3
import threading
import rospy
from local_pkg.msg import Local
from math import hypot
from time import sleep


class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        rospy.Subscriber('/local_msgs', Local, self.local_callback)
        self.period = 1.0 / rate

        self.ego = parent.shared.ego
        self.global_path = parent.shared.global_path

    def local_callback(self, msg):
        self.ego.x = msg.x
        self.ego.y = msg.y
        self.ego.heading = msg.heading
        self.ego.orientaion = msg.orientation
        self.ego.dr_x = msg.dr_x
        self.ego.dr_y = msg.dr_y
        self.ego.speed = msg.speeed
        self.ego.distance = msg.dis
        self.ego.roll = msg.roll
        self.ego.pitch = msg.pitch

    def index_finder(self):
        min_dis = -1
        min_idx = 0
        step_size = 100
        # save_idx = self.ego.index                    # for not decreasing index
        save_idx = 0
        for i in range(max(self.ego.index - step_size, 0), self.ego.index + step_size):
            try:
                dis = hypot(
                    self.global_path.x[i] - self.ego.x, self.global_path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i
                
        self.ego.index = min_idx

    def run(self):
        while True:
            self.index_finder()

            sleep(self.period)