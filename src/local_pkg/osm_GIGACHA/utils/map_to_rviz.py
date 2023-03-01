import OSMHandler
import rospy
import pymap3d
import json
import argparse
import numpy as np
from sig_Handler import ActivateSignalInterruptHandler

from visualization_msgs.msg import MarkerArray, Marker
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', nargs='*', help='file_names', default='/home/gigacha/TEAM-GIGACHA/src/local_pkg/osm_GIGACHA/output_osm/A2_LINK_output_rviz.osm', dest='file_names')
filename_input = parser.parse_args().file_names

with open('/home/gigacha/TEAM-GIGACHA/src/local_pkg/scripts/base.json')as base:
    base_data = json.load(base)

base = base_data["KCity"]
lat = base['lat']
lon = base['lon']
alt = base['alt']

# with open('../json_files/semi_final/semi_map.json') as map_data: ## SEMI FINAL PATH
    # global_path_data = json.load(map_data)
# 
with open('../json_files/final_map.json') as map_data: ## FINAL PATH
    global_path_data = json.load(map_data)

global_path_xy = global_path_data.values()

if __name__ == "__main__":
    ActivateSignalInterruptHandler()

    MAP_data = OSMHandler.OSM_data(filename_input)
    STOP_data = OSMHandler.OSM_data('/home/gigacha/TEAM-GIGACHA/src/local_pkg/osm_GIGACHA/B2_SURFACELINEMARK.osm')
    TRAFFIC_data = OSMHandler.OSM_data('/home/gigacha/TEAM-GIGACHA/src/local_pkg/osm_GIGACHA/C1_TRAFFICLIGHT.osm')

    ####### ENTIRE MAP #######
    lat_lon = []
    x_y = []

    for data in MAP_data:
        if data[0] == "node":
            lat_lon.append(data[2:4])

    lat_lon = np.array(lat_lon)

    for n, (lat_, lon_) in enumerate(lat_lon):
        x, y, _ = pymap3d.geodetic2enu(lat_, lon_, alt, lat, lon, alt)
        x_y.append([float(x), float(y)])


    ####### STOP LINE #######
    nodes = []
    nodes_dict = dict() # ids, [coordinate]

    stop_line = []
    stop_line_dict = dict() # index, [ids]

    stop_line_coordinate = dict()

    for data in STOP_data:
        if data[0] == "node":
            nodes.append(data[1:4])

        elif data[0] == "way":
            if data[4]['Kind'] == '530':
                stop_line.append(data[2])

    nodes = np.array(nodes)

    for n, (ID, lat_s, lon_s) in enumerate(nodes):
        nodes_dict[int(ID)] = [float(lat_s), float(lon_s)]

    for n, ids in enumerate(stop_line):
        stop_line_dict[n] = ids

    for n, id_list in enumerate(stop_line_dict.values()):
        stop_line_coordinate[n] = dict()
        for n_, ids in enumerate(id_list):
            stop_line_coordinate[n][ids] = nodes_dict[ids]

            x, y, _ = pymap3d.geodetic2enu(stop_line_coordinate[n][ids][0], \
            stop_line_coordinate[n][ids][1], alt, lat, lon, alt)

            stop_line_coordinate[n][ids] = [x, y]

    ####### TRAFFIC LIGHTS #######
    traffic_nodes = []
    traffic_dict = dict()

    for data in TRAFFIC_data:
        if data[0] == "node":
            Type = data[5]['Type']
            if Type == '1' or Type == '2' or Type == '3':
                traffic_nodes.append(data[1:4])

    traffic_nodes = np.array(traffic_nodes)

    for n, (ID_,lat_l, lon_l) in enumerate(traffic_nodes):
        x, y, _ = pymap3d.geodetic2enu(lat_l, lon_l, alt, lat, lon, alt)
        traffic_dict[int(ID_)] = [float(x), float(y)]
    
    ####### FOR STOP LINE RVIZ #######
    vis_dict = dict()

    for n, id_list in enumerate(stop_line_dict.values()):
        for n_, ids in enumerate(id_list):
            vis_dict[ids] = nodes_dict[ids]
            x, y, _ = pymap3d.geodetic2enu(nodes_dict[ids][0], nodes_dict[ids][1], alt, lat, lon, alt)
            vis_dict[int(ids)] = [x, y]

    ####### PARSING STOP LINE DATA #######
    j = json.dumps(stop_line_coordinate, indent = 4)
    f = open('stop_line.json', 'w')
    print(j, file = f)
    f.close()

    ####### PARSING TRAFFIC LIGHTS DATA #######
    j = json.dumps(traffic_dict, indent = 4)
    f = open('traffic_lights.json', 'w')
    print(j, file = f)
    f.close()

    ####### RVIZ #######
    rospy.init_node('map_viz', anonymous = False)
    map_pub = rospy.Publisher('/entire_map', MarkerArray, queue_size = 1)
    stop_line_pub = rospy.Publisher('/stop_line', MarkerArray, queue_size = 1)
    traffic_lights_pub = rospy.Publisher('/traffic_lights', MarkerArray, queue_size = 1)
    global_path_pub = rospy.Publisher('/global_path', Path, queue_size = 1)

    vis_path = Path()
    vis_path.header.frame_id = "map"

    checker = True
    checker_s = True
    checker_l = True
    checker_m = True

    while not rospy.is_shutdown():
        ####### MAP PUB #######
        vis_map = MarkerArray()
        c_id = 0

        for i, (x, y) in enumerate(x_y):
            map_marker = Marker()
            map_marker.header.frame_id = "map"
            map_marker.header.stamp = rospy.Time.now()
            map_marker.ns = "cubes"
            map_marker.id = c_id
            map_marker.type = Marker.CUBE
            map_marker.action = Marker.ADD
            map_marker.pose.position.z = -0.1
            map_marker.pose.orientation.x = 0.0
            map_marker.pose.orientation.y = 0.0
            map_marker.pose.orientation.z = 0.0
            map_marker.pose.orientation.w = 1.0
            map_marker.scale.z = 0.1
            map_marker.color.r = 1.0
            map_marker.color.g = 1.0
            map_marker.color.b = 1.0
            map_marker.color.a = 1.0
            map_marker.pose.position.x = x
            map_marker.pose.position.y = y
            map_marker.scale.x = 0.8
            map_marker.scale.y = 0.8
            vis_map.markers.append(map_marker)
            c_id += 1

        map_pub.publish(vis_map)

        if checker and len(vis_map.markers) != 0:
            rospy.loginfo("========MAP PUB========")
            checker = False

        ####### STOP LINE PUB #######
        vis_stop = MarkerArray()
        c_id_s = 0

        for i, (x, y) in enumerate(list(vis_dict.values())):
            stop_line_marker = Marker()
            stop_line_marker.header.frame_id = "map"
            stop_line_marker.header.stamp = rospy.Time.now()
            stop_line_marker.ns = "cubes"
            stop_line_marker.id = c_id_s
            stop_line_marker.type = Marker.CUBE
            stop_line_marker.action = Marker.ADD
            stop_line_marker.pose.position.z = -0.1
            stop_line_marker.pose.orientation.x = 0.0
            stop_line_marker.pose.orientation.y = 0.0
            stop_line_marker.pose.orientation.z = 0.0
            stop_line_marker.pose.orientation.w = 1.0
            stop_line_marker.scale.z = 0.1
            stop_line_marker.color.r = 1.0
            stop_line_marker.color.g = 0.0
            stop_line_marker.color.b = 0.0
            stop_line_marker.color.a = 1.0
            stop_line_marker.pose.position.x = x
            stop_line_marker.pose.position.y = y
            stop_line_marker.scale.x = 1.5
            stop_line_marker.scale.y = 1.5
            vis_stop.markers.append(stop_line_marker)
            c_id_s += 1

        stop_line_pub.publish(vis_stop)

        if checker_s and len(vis_stop.markers) != 0:
            rospy.loginfo("========STOP LINE PUB========")
            checker_s = False

        ####### TRAFFIC LIGHTS PUB #######
        vis_traffic = MarkerArray()
        c_id_l = 0

        for i, (x, y) in enumerate(list(traffic_dict.values())):
            traffic_lights_marker = Marker()
            traffic_lights_marker.header.frame_id = "map"
            traffic_lights_marker.header.stamp = rospy.Time.now()
            traffic_lights_marker.ns = "cubes"
            traffic_lights_marker.id = c_id_l
            traffic_lights_marker.type = Marker.CUBE
            traffic_lights_marker.action = Marker.ADD
            traffic_lights_marker.pose.position.z = -0.1
            traffic_lights_marker.pose.orientation.x = 0.0
            traffic_lights_marker.pose.orientation.y = 0.0
            traffic_lights_marker.pose.orientation.z = 0.0
            traffic_lights_marker.pose.orientation.w = 1.0
            traffic_lights_marker.scale.z = 0.1
            traffic_lights_marker.color.r = 0.0
            traffic_lights_marker.color.g = 0.0
            traffic_lights_marker.color.b = 1.0
            traffic_lights_marker.color.a = 1.0
            traffic_lights_marker.pose.position.x = x
            traffic_lights_marker.pose.position.y = y
            traffic_lights_marker.scale.x = 2.0
            traffic_lights_marker.scale.y = 2.0
            vis_traffic.markers.append(traffic_lights_marker)
            c_id_l += 1

        traffic_lights_pub.publish(vis_traffic)

        if checker_l and len(vis_traffic.markers) != 0:
            rospy.loginfo("========TRAFFIC LIGHTS PUB========")
            checker_l = False

        ####### GLOBAL PATH PUB #######
        vp = Path()
        for i, (x, y, mission) in enumerate(global_path_xy):
            read_pose = PoseStamped()
            read_pose.pose.position.x = x
            read_pose.pose.position.y = y
            read_pose.pose.position.z = 0
            read_pose.pose.orientation.x = 0
            read_pose.pose.orientation.y = 0
            read_pose.pose.orientation.z = 0
            read_pose.pose.orientation.w = 1
            vp.poses.append(read_pose)
        vis_path.poses = vp.poses

        vis_path.header.stamp = rospy.Time.now()
        global_path_pub.publish(vis_path)

        if checker_m and len(vp.poses) != 0:
            rospy.loginfo("========GLOBAL PATH PUB========")
            checker_m = False

        rate = rospy.Rate(1)

        rate.sleep()