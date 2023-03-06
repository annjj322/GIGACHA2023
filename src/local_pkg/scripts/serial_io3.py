#!/usr/bin/env python3
from sig_int_handler import Activate_Signal_Interrupt_Handler
import serial
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
import threading
import struct
import rospy

class Serial_IO:
    def __init__(self):
        self.count = 0
        self.count2 = 0

        ################### JMGAY : No TOUCH!! ####################
        ###########################################################
        # Serial Connect
        self.ser = serial.Serial("/dev/erp42", 115200) # Real World

        # ROS Publish
        rospy.init_node("Serial_IO", anonymous=False)
        self.serial_pub = rospy.Publisher("/serial", Serial_Info, queue_size=1)
       
        # Messages/Data
        self.serial_msg = Serial_Info()  # Message o publish
        self.alive = 0

        #Subscribe Control Info from Controller
        self.control_input = Control_Info()
        self.emergency_stop = 0
        self.gear = 0

        # Serial Read Thread
        th_serialRead = threading.Thread(target=self.serialRead)
        th_serialRead.daemon = True
        th_serialRead.start()

        # rospy Rate
        rt = 20
        rate = rospy.Rate(rt)
        #############################################################
        #############################################################


        ### touch me... haang...
        self.control_input.speed = 20 # chogi speed
        self.control_input.steer = 2 # chogi steer : going a little left when steer is 0, so 1(change it!)
        self.control_input.brake = 0 # chogi brake
     
        # Main Loop
        sprint_time_sec = 3 # touch me!
        change_sec = 0.75 # touch me!
#######################################only brake control ###########################################
        # while not rospy.is_shutdown():
        #     self.serialWrite()
        #     self.count += 1
        #     self.count2 += 1
        #     if self.count2>=sprint_time_sec*rt and self.count%change_sec*rt==0: 
        #         self.control_input.brake+=10
        #    rate.sleep()
######################################################################################                
        # while not rospy.is_shutdown():
        #     self.serialWrite()
        #     self.count += 1
        #     self.count2 += 1
        #     if self.count2>=sprint_time_sec*rt and self.count%change_sec*rt==0:
        #         self.control_input.brake+=10
        #         self.control_input.speed-=1
        #     rate.sleep()
######################################################################################                
        value = 2
        maxbrake = 30
        while not rospy.is_shutdown():
            self.serialWrite()
            self.count += 1
            self.count2 += 1
            self.control_input.brake = 20
            if self.control_input.speed>3: 
                if self.count2>=(sprint_time_sec*rt) and self.count%(change_sec*rt)==0: 
                    self.control_input.brake-=value
                    self.control_input.speed-=value
            else:
                self.control_input.speed = 3
                self.control_input.brake = 0
                
            rate.sleep()

    def serialRead(self):
        print("Serial_IO: Serial reading thread successfully started")

        while True:
            
            print(f"Serial_IO: Reading serial {self.alive}")
            print("Current speed is : ", self.control_input.speed)
            print("Current brake is : ", self.control_input.brake)
            packet = self.ser.read_until(b'\x0d\x0a')
            # print(len(packet))
            if len(packet) == 18:
                header = packet[0:3].decode()

                if header == "STX":
                    #auto_manual, e-stop, gear
                    (self.serial_msg.auto_manual,
                    self.serial_msg.emergency_stop,
                    self.serial_msg.gear) \
                    = struct.unpack("BBB", packet[3:6])
                    
                    #speed, steer
                    tmp1, tmp2 = struct.unpack("2h", packet[6:10])
                    self.serial_msg.speed = tmp1 / 10  # km/h

                    self.serial_msg.steer = tmp2 / 71  # degree


                    self.alive = struct.unpack("B", packet[15:16])[0]

                    self.serial_pub.publish(self.serial_msg)

    def serialWrite(self):
        #Min/Max Limit
        if self.control_input.speed > 20:
            self.control_input.speed = 20

        self.control_input.speed = max(0, min(self.control_input.speed, 20))

        if self.control_input.brake > 200:
            self.control_input.brake = 200

        result = struct.pack(
            ">BBBBBBHhBBBB",
            0x53,
            0x54,
            0x58,
            1, #always auto
            self.control_input.emergency_stop,
            self.control_input.gear,
            int(self.control_input.speed * 10),
            # int(self.control_input.speed * 10),
            int(self.control_input.steer * 71),
            # 100,
            self.control_input.brake,
            self.alive,
            0x0D,
            0x0A
        )
        
        self.ser.write(result)


    # def controlCallback(self, msg):
    #     self.control_input = msg

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    erp = Serial_IO()
