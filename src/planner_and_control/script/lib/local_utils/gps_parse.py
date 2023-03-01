#!/usr/bin/env python3
import serial
import rospy

from planner_and_control.msg import Gngga

class GNGGA_Parsing:
    def __init__(self):
        self.ser = serial.Serial('/dev/gps', baudrate = 115200)
        print('GNGGA_Parsing : Serial connecting to /dev/gps')

        self.gngga_msg = Gngga()
        rospy.init_node("Gngga_data", anonymous=False)
        self.pub = rospy.Publisher("/Gngga_raw", Gngga, queue_size=1)

        self.lat = 0.0
        self.lon = 0.0
        self.status = ""
        self.satellite = ""
        self.noise = ""
        self.data = ""


    def parese_gngga(self):
        ser_read = self.ser.readline()
        try:
            self.data = ser_read.decode('ascii')
        except:
            UnicodeDecodeError

        # print(self.data)

        if self.data[0:6] == "$GNGGA":
            sdata = self.data.split(",")
            
            if sdata[6] == "0":
                print("GNGGA_Parsing : No satellite data available")
                return

            print("=========Parsing GNGGA=========")
            print("latitude : {}".format(self.lat))
            print("longitude : {}".format(self.lon))
            self.lat = self.lat_decode(sdata[2])
            self.lon = self.lon_decode(sdata[4])
            self.status = sdata[6]
            self.satellite = sdata[7]
            self.noise = sdata[8]

            self.gngga_msg.latitude = self.lat
            self.gngga_msg.longitude = self.lon
            self.gngga_msg.quality_indicator = self.status

            self.pub.publish(self.gngga_msg)

    def lat_decode(self, coord):
        lat_deg = float(coord[0:2])
        lat_min = float(coord[2:]) / 60

        return lat_deg + lat_min

    def lon_decode(self, coord):
        lon_deg = float(coord[0:3])
        lon_min = float(coord[3:]) / 60

        return lon_deg + lon_min

if __name__ == "__main__":
    gps = GNGGA_Parsing()

    while not rospy.is_shutdown():
        gps.parese_gngga()
