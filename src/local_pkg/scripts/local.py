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


class Localization():
    def __init__(self, base): # subscriber, 변수
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

    def heading_decision(self): # imu, gps 헤딩을 이용한 최종 헤딩 결정
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

    def main(self):
        self.heading_decision() # 헤딩 계산

        orientation = list(quaternion_from_euler(
            self.imu.roll, self.imu.pitch, self.heading)) # roll, pitch, yaw 오일러 각을 쿼터니안 각으로 변환해 orientation 결정

        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.hAcc = self.gps.hAcc
        self.msg.speeed = self.dr.speed
        self.msg.dis = self.dr.pulse / 58.82

        if self.master_switch:
            if 0 < self.gps.hAcc < 50: # gps 정확도가 높으면 dead reckoning 수행 안하고 gps 값 참조
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
        self.msg.orientation.w = orientation[3] # 변수들에 최종값 담기
        # print('rawx, y ',self.gps.raw_x,self.gps.raw_y)
        self.pub.publish(self.msg) # msg로 publish

        rospy.loginfo(self.msg)
        # rospy.loginfo(self.msg.heading)


if __name__ == '__main__': # 실행
    Activate_Signal_Interrupt_Handler()

    parser = argparse.ArgumentParser() # argument 받아 와 parsing(base 이름)
    parser.add_argument('--base', '-b', nargs='*',
                        help='base_names', default=[], dest='base_names')
    basename_input = parser.parse_args().base_names

    if len(basename_input) == 0:
        base_name = "KCity"

    elif len(basename_input) == 1:
        base_name = basename_input[0] # input 받아와 argument로 설정

    else:
        raise Exception('Invalid Arguments')

    loc = Localization(base_name)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()
