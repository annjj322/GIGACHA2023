#!/usr/bin/env python3
import json
import threading
import csv
import rospy
from local_pkg.msg import Local
from math import hypot
from time import sleep

class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        rospy.Subscriber('/local_msgs', Local, self.local_callback)

        self.mapname = parent.args.map
        self.period = 1.0 / rate

        self.ego = parent.shared.ego
        self.global_path = parent.shared.global_path
        self.perception = parent.shared.perception
        self.read_global_path()  # only one time
        self.hAcc = 100000
        self.x = 0
        self.y = 0

    def local_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.hAcc = msg.hAcc
        self.ego.speed = msg.speeed
        self.ego.heading = msg.heading
        self.ego.orientaion = msg.orientation
        self.ego.dr_x = msg.dr_x
        self.ego.dr_y = msg.dr_y
        self.ego.roll = msg.roll
        self.ego.pitch = msg.pitch
        self.ego.dis = msg.dis

        self.ego.x = msg.x
        self.ego.y = msg.y
        
    def read_global_path(self):
        with open(f"maps/{self.mapname}.json", 'r') as json_file:
            json_data = json.load(json_file)
            for n, (x, y , mission, map_speed) in enumerate(json_data.values()):
                self.global_path.x.append(x)
                self.global_path.y.append(y)
                self.global_path.mission.append(mission)
                self.ego.map_speed.append(map_speed)

    def index_finder(self):
        min_dis = -1
        min_idx = 0
        step_size = 50
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
        
        self.perception.signname = self.global_path.mission[self.ego.index]

    def dead_reckoning(self):
        if self.hAcc < 50 :
            self.ego.x = self.x
            self.ego.y = self.y
        else:
            self.ego.x = self.ego.dr_x
            self.ego.y = self.ego.dr_y

    def run(self):
        while True:
            self.index_finder()
            self.dead_reckoning()

            sleep(self.period)
