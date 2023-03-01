#!/usr/bin/env python3
import serial
import rospy
import signal
from std_msgs.msg import Int64
from sig_int_handler import Activate_Signal_Interrupt_Handler

class Encoder_Parsing():
    def __init__(self):
        rospy.init_node('Displacement_right', anonymous = False)
        self.pub = rospy.Publisher('/Displacement_right', Int64, queue_size = 1)
        self.ser = serial.Serial(port = '/dev/encoder', baudrate = 115200)
        self.init_data = 0

    def main(self):
        res = self.ser.readline()
        while True:
            try:
                self.init_data = int(res)
                rospy.loginfo(int(res))
                break
            except:
                res = self.ser.readline()

        self.pub.publish(int(res))

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    enc = Encoder_Parsing()

    while not rospy.is_shutdown():
        enc.main()