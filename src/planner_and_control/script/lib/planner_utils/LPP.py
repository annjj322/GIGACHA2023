# -*- coding: utf-8 -*-
from nav_msgs.msg import Path
from planner_and_control.msg import Path as CustomPath
from geometry_msgs.msg import PoseStamped
import numpy as np
from math import cos,sin,atan2
from time import sleep

def path_maker(local_path, ego):
    out_path=[]
    ref_local_path = CustomPath()

    print("len(local_path.poses) : ", len(local_path.poses))
    print("local_path.poses : ", local_path.poses)
    for i in range (len(local_path.poses)):
        ref_local_path.x.append(local_path.poses[i].pose.position.x)
        ref_local_path.y.append(local_path.poses[i].pose.position.y)
    print("len(ref_local_path.x :", len(ref_local_path.x))

    current_x = ego.x
    current_y = ego.y
    current_speed = ego.speed

    look_distance = int(current_speed * 2)

    if look_distance < 2 :
        look_distance = 2
    if look_distance > 10 :
        look_distance = 10
    
    look_distance = 35
    # print("사람이있다니까요")
    # print("len(ref_local_path.x :", len(ref_local_path.x))
    # print("look_distacne : ", look_distance)
    # print("사람이여기또있어요")
    # sleep(5)
    if len(ref_local_path.x) > look_distance :
        global_ref_start_point = (ref_local_path.x[0], ref_local_path.y[0])
        global_ref_start_next_point = (ref_local_path.x[1], ref_local_path.y[1])
        global_ref_end_point = (ref_local_path.x[look_distance], ref_local_path.y[look_distance])
        
        theta = atan2(global_ref_start_next_point[1]-global_ref_start_point[1], global_ref_start_next_point[0]-global_ref_start_point[0])
        translation = [global_ref_start_point[0], global_ref_start_point[1]]

        t = np.array([[cos(theta), -sin(theta), translation[0]], [sin(theta), cos(theta), translation[1]], [0,0,1]])
        det_t = np.array([[t[0][0], t[1][0], -(t[0][0] * translation[0] + t[1][0] * translation[1])], [t[0][1], t[1][1], -(t[0][1] * translation[0] + t[1][1] * translation[1])], [0,0,1]])

        world_end_point = np.array([[global_ref_end_point[0]], [global_ref_end_point[1]], [1]])
        local_end_point = det_t.dot(world_end_point)
        world_current_point = np.array([[current_x], [current_y], [1]])
        local_current_point = det_t.dot(world_current_point)

        lane_off_set = [2.5, 0, -2.5]
        local_lattice_points = []
        for i in range(len(lane_off_set)):
            local_lattice_points.append([local_end_point[0][0], local_end_point[1][0] + lane_off_set[i], 1])

        for end_point in local_lattice_points:
            lattice_path = Path()
            lattice_path.header.frame_id = 'map'
            x = []
            y = []
            x_interval = 0.5
            xs = 0
            xf = end_point[0]
            ps = local_current_point[1][0]

            pf = end_point[1]
            x_num = xf / x_interval

            for i in range(xs, int(x_num)): 
                x.append(i * x_interval)
            
            a = [0.0,0.0,0.0,0.0,0.0,0.0]
            a[0] = ps
            a[1] = 0
            a[2] = 0
            a[3] = 10.0 * (pf-ps) / (xf * xf * xf)
            a[4] = -15.0 * (pf-ps) / (xf * xf * xf * xf)
            a[5] = 6.0 * (pf-ps) / (xf * xf * xf * xf * xf)
            


            for i in x:
                result =a[5]*i*i*i*i*i + a[4]*i*i*i*i + a[3]*i*i*i + a[2]*i*i + a[1]*i + a[0]
                y.append(result)

            for i in range(0, len(y)):
                local_result = np.array([[x[i]], [y[i]], [1]])
                global_result = t.dot(local_result)

                read_pose = PoseStamped()
                read_pose.pose.position.x = global_result[0][0]
                read_pose.pose.position.y = global_result[1][0]
                read_pose.pose.position.z = 0
                read_pose.pose.orientation.x = 0
                read_pose.pose.orientation.y = 0
                read_pose.pose.orientation.z = 0
                read_pose.pose.orientation.w = 1

                lattice_path.poses.append(read_pose)

            print("path maker : lattice path; ", lattice_path)
            out_path.append(lattice_path)
        
        add_point_size = int(current_speed * 4)
        
        #if add_point_size > len(ref_local_path.x) - 2:
            #add_point_size = len(ref_local_path.x)
        add_point_size = 75

        if add_point_size > len(ref_local_path.x) - 2:
            add_point_size = len(ref_local_path.x)

        elif add_point_size < 5 :
            add_point_size = 5  
         
        for i in range(look_distance, add_point_size):
            if i + 1 < len(ref_local_path.x):
                tmp_theta = atan2(ref_local_path.y[i+1] - ref_local_path.y[i], ref_local_path.x[i+1] - ref_local_path.x[i])
                
                tmp_translation = [ref_local_path.x[i], ref_local_path.y[i]]
                tmp_t = np.array([[cos(tmp_theta), -sin(tmp_theta), tmp_translation[0]], [sin(tmp_theta), cos(tmp_theta), tmp_translation[1]], [0,0,1]])

                for lane_num in range(3):
                    local_result = np.array([[0], [lane_off_set[lane_num]], [1]])
                    global_result = tmp_t.dot(local_result)

                    read_pose = PoseStamped()
                    read_pose.pose.position.x = global_result[0][0]
                    read_pose.pose.position.y = global_result[1][0]
                    read_pose.pose.position.z = 0
                    read_pose.pose.orientation.x = 0
                    read_pose.pose.orientation.y = 0
                    read_pose.pose.orientation.z = 0
                    read_pose.pose.orientation.w = 1
                    out_path[lane_num].poses.append(read_pose)
    return out_path