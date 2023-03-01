import numpy as np
import csv
import rospy
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32


def csv_to_map():
    map_x = []
    map_y = []
    with open("/home/gigacha/Phase1_Team2/src/final_pkg/scripts/lib/new_mapping/maps/merge.csv", mode="r") as csv_file:

        for line in csv_file.readlines():
            array = line.split(',')
            if line == 0:
                map_x = float(array[0])
                map_y = float(array[1])
            else:
                map_x.append(float(array[0]))
                map_y.append(float(array[1]))


    rospy.init_node("csv_to_map",anonymous = True)
    pub = rospy.Publisher("/rviz_map", PointCloud, queue_size = 1)

    csv_path = PointCloud()
    csv_path.header.frame_id = "map"
    csv_path.header.stamp = rospy.Time.now()

    for i in range(len(map_x)):
        path = Point32()
        path.x = map_x[i] + 10000
        path.y = map_y[i] - 16000
        csv_path.points.append(path)

    pub.publish(csv_path)

while not rospy.is_shutdown():
    csv_to_map()
