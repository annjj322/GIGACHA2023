from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from math import sqrt
from time import sleep

def findLocalPath(path, ego):
    out_path = Path()
    current_x = ego.x
    current_y = ego.y
    current_index = 0
    min_dis = float('inf')

    for i in range(len(path.x)):
        dx = current_x - path.x[i]
        dy = current_y - path.y[i]
        dis = sqrt(dx*dx + dy*dy)
        if dis < min_dis:
            min_dis = dis
            current_index = i
    
    if current_index + 100 > len(path.x):
        last_local_index = len(path.x)
    else:
        last_local_index = current_index + 100

    for i in range(current_index, last_local_index) :
        read_pose = PoseStamped()

        read_pose.pose.position.x = path.x[i]
        read_pose.pose.position.y = path.y[i]
        read_pose.pose.position.z = 0
        read_pose.pose.orientation.x = 0
        read_pose.pose.orientation.y = 0
        read_pose.pose.orientation.z = 0
        read_pose.pose.orientation.w = 1

        out_path.poses.append(read_pose)
    print("find local paath out_path.poses len ", len(out_path.poses))

    return out_path
