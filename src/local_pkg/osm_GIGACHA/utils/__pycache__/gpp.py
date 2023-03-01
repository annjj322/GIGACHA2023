import OSMHandler
import pymap3d
import numpy as np
import argparse
import json
from sig_Handler import ActivateSignalInterruptHandler
from pyroutelib3 import Router

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class Global_path_planning():
    def __init__(self, file_name, start_node, end_node, mission):
        self.file_name = file_name
        self.mission = mission

        self.nodes = []
        self.nodes_dict = dict()

        self.ways = []
        self.ways_dict = dict()

        self.path = []
        self.path_dict = dict()

        self.osm_data = OSMHandler.OSM_data(self.file_name)

        self.router = Router('car', self.file_name)
        self.start_node = start_node
        self.end_node = end_node

        with open('/home/gigacha/TEAM-GIGACHA/src/local_pkg/scripts/base.json')as base:
            base_data = json.load(base)
        
        self.base = base_data["KCity"]
        self.lat = self.base['lat']
        self.lon = self.base['lon']
        self.alt = self.base['alt']

        self.osm_to_dict()
        self.path_planning(self.mission)


    def osm_to_dict(self):
        for data in self.osm_data:
            if data[0] == 'node':
                self.nodes.append(data[1:4]) # id, lat, lon
            elif data[0] == 'way':
                self.ways.append(data[1:3]) # id, nodes
        
        self.ndoes = np.array(self.nodes)

        for n, (ID, lat, lon) in enumerate(self.nodes):
            self.nodes_dict[int(ID)] = [float(lat), float(lon)]
        
        for n, (ID, nodes) in enumerate(self.ways):
            self.ways_dict[int(ID)] = nodes

    def path_planning(self, mission_name):
        start = self.router.findNode(self.nodes_dict[self.start_node][0],\
        self.nodes_dict[self.start_node][1])
        
        end = self.router.findNode(self.nodes_dict[self.end_node][0],\
        self.nodes_dict[self.end_node][1])

        status, route = self.router.doRoute(start, end)

        if status == "success":
            self.path = route # ids

            for i, ids in enumerate(self.path):
                x, y, _ = pymap3d.geodetic2enu(self.nodes_dict[ids][0], self.nodes_dict[ids][1], self.alt, self.lat, self.lon, self.alt)
                self.path_dict[i] = [float(x), float(y)]
                self.path_dict[i].append(mission_name)

            for n, (ID, lat, lon) in enumerate(self.nodes):
                x, y, _ = pymap3d.geodetic2enu(lat, lon, self.alt, self.lat, self.lon, self.alt)
                self.nodes_dict[int(ID)] = [float(x), float(y)]

        else:
            print("CAN'T FIND A PATH")

        j = json.dumps(self.path_dict, indent = 4)
        f = open('final_path5.json', 'w')
        print(j, file = f)
        f.close()

if __name__ == '__main__':
    ActivateSignalInterruptHandler()

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '--f', nargs='*', help='file_names', default='/home/gigacha/TEAM-GIGACHA/src/local_pkg/osm_GIGACHA/output_osm/A2_LINK_output.osm', dest='file_names')
    
    filename_input = parser.parse_args().file_names

    global_path_planning = Global_path_planning(filename_input, -165620, -905257,'driving')

    print("==================COMPLETE==================")