#!/usr/bin/env python3
import time
import rospy
import math
import argparse
from local_pkg.msg import Local
from nav_msgs.msg import Path
from gps import GPS
from ahrs import IMU
from odometry import DR
from local_functions import quaternion_from_euler
from sig_int_handler import Activate_Signal_Interrupt_Handler
from collections import deque

class Localization():
    def __init__(self, base):
        rospy.init_node('Localization', anonymous=False)
        rospy.Subscriber("/vis_global_path", Path, self.masterCallback)

        self.pub = rospy.Publisher('/local_msgs', Local, queue_size=1)
        self.msg = Local()
        self.base = base

        self.gps = GPS(self.base)
        self.imu = IMU()
        self.dr = DR()

        self.offset = 0
        self.heading = 0.0

        self.master_switch = False
        self.dr_init = False
        self.last_pulse = 0

        self.dead_heading = 0.0

    def masterCallback(self, msg):
        self.master_switch = True

    def heading_decision(self):
        global time_sync
        main_time = time.time()
        time_sync = None

        if self.dr.gear == 0:

            if (main_time - self.gps.time) < 0.2 and (main_time - self.imu.time) < 0.2:
                time_sync = "Sync"
                if self.gps.heading_switch == True:
                    self.offset = self.gps.heading - self.imu.heading
                    self.heading = (self.imu.heading + self.offset)
                else:
                    self.heading = (self.imu.heading + self.offset)
            else:
                time_sync = "Unsync"
                self.heading = (self.imu.heading + self.offset)

        else:
            self.heading = (self.imu.heading + self.offset)
        
        
    def true_heading(self):
        recent_heading = deque(maxlen=3)

        recent_heading.append(self.heading)

        heading_offset = 130
        
        last = recent_heading[0]
        
        if abs(last - self.heading) > heading_offset :
            self.heading = last
            recent_heading.append(last)
        else :
            recent_heading.append(self.heading) # if gear == 2 !!
        

    def main(self):
        self.heading_decision()
        self.true_heading()
        orientation = list(quaternion_from_euler(
            self.imu.roll, self.imu.pitch, self.heading))

        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.hAcc = self.gps.hAcc
        # self.msg.speeed = self.dr.speed
        self.msg.speeed = 0
        self.msg.gspeed = self.gps.gspeed *0.0036 # [km/h]
        self.msg.dis = self.dr.pulse / 58.82

        if self.master_switch:
            if 0 < self.gps.hAcc < 50:
                self.msg.dr_x = self.gps.x
                self.msg.dr_y = self.gps.y
                self.dr_init = False

            else:
                if not self.dr_init:
                    self.last_pulse = self.dr.pulse
                    self.dr_init = True

                if self.gps.heading_switch == True and self.dr_init:
                    if self.dr.gear == 0:
                        self.dead_heading = self.heading
                    elif self.dr.gear == 2:
                        self.dead_heading = (self.heading + 180) % 360

                    self.diff_pulse = self.dr.pulse - self.last_pulse
                    dis = self.diff_pulse / 58.82

                    self.msg.dr_x += dis * \
                        math.cos(math.radians(self.dead_heading))
                    self.msg.dr_y += dis * \
                        math.sin(math.radians(self.dead_heading))
                    self.last_pulse = self.dr.pulse

        self.msg.roll = self.imu.roll
        self.msg.pitch = self.imu.pitch
        self.msg.heading = self.heading
        self.msg.orientation.x = orientation[0]
        self.msg.orientation.y = orientation[1]
        self.msg.orientation.z = orientation[2]
        self.msg.orientation.w = orientation[3]

        self.pub.publish(self.msg)

        rospy.loginfo(self.msg)
        # rospy.loginfo(self.msg.heading)


if __name__ == '__main__':
    Activate_Signal_Interrupt_Handler()

    parser = argparse.ArgumentParser()
    parser.add_argument('--base', '-b', nargs='*',
                        help='base_names', default=[], dest='base_names')
    basename_input = parser.parse_args().base_names

    if len(basename_input) == 0:
        base_name = "Songdo" #"KCity"       

    elif len(basename_input) == 1:
        base_name = basename_input[0]

    else:
        raise Exception('Invalid Arguments')

    loc = Localization(base_name)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()
    if len(basename_input) == 0:
        base_name = "Songdo" #"KCity"