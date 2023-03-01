# from planner_and_control.msg import Path
# import csv
# from numpy import rad2deg

# def read_global_path(folder, name):
#     global_path = Path()
#     with open("/home/gigacha/TEAM-GIGACHA/src/planner_and_control/script/lib/mapping_utils/maps/" + folder + "/" + name + ".csv", mode="r") as csv_file:
#         csv_reader = csv.reader(csv_file)
#         for line in csv_reader:
#             global_path.x.append(float(line[0]))
#             global_path.y.append(float(line[1]))
#             #global_path.k.append(float(line[2]))
#     return global_path

################# jy gay & hw gay modified #########################

import json
import rospy
from planner_and_control.msg import Path
from planner_and_control.msg import Local


def read_global_path(folder, name):
    global_path = Path()
    with open("/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/kcity_simul/semi_map.json", mode="r") as json_file:
    # with open(f"maps/{self.mapname}.json", 'r') as json_file:
        json_data = json.load(json_file)
        for n, (x, y, mission, map_speed) in enumerate(json_data.values()):
            global_path.x.append(x)
            global_path.y.append(y)
            # ego.map_speed.append(map_speed)
            
    
    return global_path
