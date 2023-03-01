from ast import Str
import rospy
from std_msgs.msg import String
from planner_and_control.msg import Path, Control_Info, Ego, Perception

class State_hub:
    def __init__(self):
        rospy.init_node('State_Hub', anonymous = False)

        rospy.Subscriber('/state', String, self.state_callback) #mission
        rospy.Subscriber('/behavior', String, self.behavior_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback) #behavior
        rospy.Subscriber('/trajectory', Path, self.motion_callback) 
        rospy.Subscriber('/controller',Control_Info, self.control_callback)
        rospy.Subscriber('/perception',Perception, self.perception_callback)
        self.state = ""
        self.behavior = ""
        self.motion = Path()
        self.control_msg = Control_Info()
        self.ego = Ego()
        self.control = Control_Info()
        self.perception = Perception()

    def ego_callback(self, msg):
        self.ego.x = msg.x

    def state_callback(self, msg):  #mission_planner callback
        self.state = msg.data

    def behavior_callback(self, msg):  #behavior_planner
        self.behavior = msg.data

    def motion_callback(self, msg):
        self.motion = msg

    def control_callback(self, msg):
        self.control = msg

    def perception_callback(self, msg):
        self.perception = msg

    def run(self):
        print("------------------------------------------------------")
        print("\n[map_name]")
        print(self.ego.map_file)
        print("\n[mission_planner]")
        print(self.state)
        print("\n[behavior_planner]")
        print(self.behavior)
        print("\n[motion_planner]")
        print("select line : " + str(self.motion.select_lane)) 
        print("\n[controll_info]")
        print(self.control)
        print("\n[sign_name]")
        print(self.perception.signname)
        print("------------------------------------------------------")

if __name__ == "__main__":
    A = State_hub()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        A.run()
        rate.sleep