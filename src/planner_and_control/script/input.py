import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Perception

class Input:
    def __init__(self):
        rospy.init_node('Input', anonymous = False)
        self.pub = rospy.Publisher("/input", Perception, queue_size = 1)
        self.perception = Perception()
        self.perception.signname = " "
        self.perception.tred = False
        self.perception.tyellow = False
        self.perception.tleft = False
        self.perception.tgreen = False
        self.perception.objx = []
        self.perception.objy = []
        self.perception.objr = []
        self.perception.signx = []
        self.perception.signy = []
        self.perception.tred = 0
        self.perception.tyellow = 0
        self.perception.tleft = 0
        self.perception.tgreen = 0
        self.perception.signname = "go"
    
    def function(self):
        self.mission = int(input("which mission? (0: obstacle, 1: turn_right, 2: child, 3: turn_left, 4: delivery, 5 : non_traffic_light turn_right) : "))
        if(self.mission == 0):
            x = float(input("object x : "))
            y = float(input("object y : "))
            r = float(input("object r : "))
            self.perception.objx.append(x)
            self.perception.objy.append(y)
            self.perception.objr.append(r)
            self.perception.signname = "static_obstacle"

            print(f"x : {self.perception.objx}, y : {self.perception.objy}, r : {self.perception.objr}")

        elif (self.mission == 1):
            self.perception.tred = int(input("red(on : 1, off : 0) : "))
            self.perception.tyellow = int(input("yellow(on : 1, off : 0) : "))
            self.perception.tleft = int(input("left(on : 1, off : 0) : "))
            self.perception.tgreen = int(input("green(on : 1, off : 0) : "))
            self.perception.signname = "turn_right_traffic_light"

        elif (self.mission == 2):
            self.perception.signname = "child_area"
            x = float(input("signx : "))
            y = float(input("signy : ")) 
            self.perception.signx.append(x)
            self.perception.signy.append(y)
            
        elif (self.mission == 3):
            self.perception.tred = int(input("red(on : 1, off : 0) : "))
            self.perception.tyellow = int(input("yellow(on : 1, off : 0) : "))
            self.perception.tleft = int(input("left(on : 1, off : 0) : "))
            self.perception.tgreen = int(input("green(on : 1, off : 0) : "))
            self.perception.signname = "turn_left_traffic_light"

        elif (self.mission == 4):
            self.perception.signname = "delivery"

        elif (self.mission == 5):
            self.perception.signname = "non_traffic_right"
        
        else:
            self.perception.signname = " "
        
    def run(self):
        self.pub.publish(self.perception)
        self.function()
        print("input_mission : ",self.perception.signname)
        
if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    ss = Input()
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep