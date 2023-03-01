import rospy, math
from local_pkg.msg import Local
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from local_pkg.msg import Master

rospy.init_node("data_publisher", anonymous = False)

local_data = Local()
serial_data = Serial_Info()
control_data = Control_Info()
master_data = Master()

local_pub = rospy.Publisher("/local_msgs", Local, queue_size = 1)
serial_pub = rospy.Publisher("/serial", Serial_Info, queue_size = 1)
control_pub = rospy.Publisher("/controller", Control_Info, queue_size = 1)
master_pub = rospy.Publisher("/from_master", Master, queue_size = 1)


local_data.dr_x = 23.33
local_data.dr_y = 23.33

serial_data.speed = 15
serial_data.auto_manual = 1

control_data.gear = 2
control_data.steer = 15

master_data.mission = "drving"
master_data.behavior = "go"
master_data.localizer = True
master_data.mission_pln = False
master_data.behavior_pln = True
master_data.motion_pln = False
master_data.lat_con = False
master_data.lon_con = True

rate = rospy.Rate(10)

while not rospy.is_shutdown():
    for i in range(10000):
        local_data.x += 1
        local_data.y += 1
        local_data.heading += 1
        local_pub.publish(local_data)

    serial_pub.publish(serial_data)
    control_pub.publish(control_data)
    master_pub.publish(master_data)

    rate.sleep()