#!/usr/bin/env python3
import serial
import rospy

from sensor_msgs.msg import Imu

class AHRS_Parsing:
    def __init__(self):
        self.ser = serial.Serial('/dev/imu', baudrate = 115200)
        rospy.init_node("imu_raw", anonymous=False)
        print('AHRS_Parsing : Serial connecting to /dev/imu')

        self.raw_data = Imu()
        self.raw_data.header.stamp = rospy.Time.now()
        self.raw_data.header.frame_id = "imu_link"
        self.pub = rospy.Publisher("/imu", Imu, queue_size=1)
        self.data = ""

    def parser(self):
        ser_read = self.ser.readline()
        try:
            self.data = ser_read.decode('ascii')
        except:
            UnicodeDecodeError

        sdata = self.data.split(",")
        self.raw_data.orientation.x = float(sdata[3])
        self.raw_data.orientation.y = float(sdata[2])
        self.raw_data.orientation.z = float(sdata[1])
        self.raw_data.orientation.w = float(sdata[4])
        self.raw_data.angular_velocity.x = float(sdata[5])

        self.pub.publish(self.raw_data)
        print(self.raw_data)


if __name__ == "__main__":
    imu = AHRS_Parsing()

    while not rospy.is_shutdown():
        imu.parser()