from math import sqrt
from math import sqrt
from math import cos,sin,atan2
import numpy as np
from shared.path import Path

class Motion():
    def __init__(self, sh, pl, eg):
        self.shared = sh
        self.plan = pl
        self.ego = eg

        self.global_path = self.shared.global_path # from localizer
        self.cut_path = self.shared.cut_path # from global path (find_local_path)
        self.lattice_path = self.shared.lattice_path # from LPP []

        self.lane_offset = [5.4, 4.35, 3.3, 2.75, 2.2, 1.7, 1.2, 0.2, 0, -0.25, -0.7, -1.45, -2.2] # for kcity map # 원래 장애물 회피를 위한 오프셋임. 0인 lane이 없어서 주차 때는 아래를 사용
        self.lane_weight = None

    def select_trajectory(self):
        self.shared.selected_lane = self.lane_weight.index(min(self.lane_weight))
        # self.shared.selected_lane = 7
        # if self.shared.ego.target_gear == 2:
        #     self.shared.selected_lane = 9
        # elif self.shared.plan.behavior_decision == "parkingForwardOn":
        #     self.shared.selected_lane = 8
        # elif self.shared.ego.target_gear == 2 and self.shared.plan.behavior_decision == "parkingForwardOn":
        #     self.shared.selected_lane = 8
        # print("lane : ", self.shared.selected_lane)

    def static_obstacle_aviodance(self):
        # 5/5 일단 정적 장애물부터
        # ㄴ정적 장애물 -완-
        path_weight = [100.5, 40.4, 25.3, 10.2, 0.1, 10.2, 100.3]
        obs_1 = [66.9928, 50.4973, 5, 649] # [x, y, lane, closest index]
        obs_2 = [70.6899, 61.4106, 3, 762]
        obs_3 = [80.1545, 77.3181, 4, 948]
        obs_list = [obs_1, obs_2, obs_3] 
        for obs in obs_list:
            if obs[3]+3<self.shared.ego.index:
                continue
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)
            obs_value = [100/distance, 200/distance, 100/distance]
            if 0<obs[2]<len(path_weight):
                path_weight[obs[2]-1] += obs_value[0]
                path_weight[obs[2]] += obs_value[1]
                path_weight[obs[2]+1] += obs_value[2]

        print(list(np.round(path_weight)))
        print("INDEX : ", self.shared.ego.index)
        print(self.shared.ego.x)
        print(self.shared.ego.y)
        return path_weight

    def dynamic_obstacle_aviodance(self):
        path_weight = [100.5, 90.4, 25.3, 10.2, 0.1, 10.2, 100.3]
        obs_1_start = [97.01, 104.32, 5, 1266]
        obs_1_middle_1 = [93.91, 103.9, 4, 1248]
        obs_1_middle_2 = [92.57, 103.58, 3, 1239]
        obs_1_end = [89.18, 103.03, 2, 1219]
        obs_1_list = [obs_1_start, obs_1_middle_1, obs_1_middle_2, obs_1_end] 
        gain = 0.3
        for obs in obs_1_list:
            if obs_1_start[3]+10 < self.shared.ego.index:
                break
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)
            print("distance : ", distance)
            obs_value = [100/(distance**0.5)*gain, 200/(distance**0.5)*gain, 100/(distance**0.5)*gain]
            if 0<obs[2]<len(path_weight):
                print(obs_value)
                path_weight[obs[2]-1] += obs_value[0]
                path_weight[obs[2]] += obs_value[1]
                path_weight[obs[2]+1] += obs_value[2]
            
            gain += 0.1

        print("Weight : ", list(np.round(path_weight, 1)))
        # print("asdfasdfasdf : ", self.shared.ego.index)
        # print(self.shared.ego.x)
        # print(self.shared.ego.y)
        return path_weight

    def all_obstacle_aviodance(self):
        """
        This function calculates the optimal path for a vehicle to navigate through a set of static and dynamic obstacles.

        Case 1 -> started from the right, slow object
        Case 2 -> started from the left, fast object
        Case 3 -> started from the left, slow object
        Case 4 -> started from the right, fast object

        Args:
        - obstacle_list: A list containing the position and size of each obstacle. Each list should have x, y, lane, closest index
        - lane_weight: A float that represents the weight of the lane. It determines the cost of traveling through each lane. The default value is 8 (index).
        
        Returns:
        - A list representing the weights for the vehicle to navigate through the obstacles.
        """
        path_weight = [1000, 14, 12, 10, 8, 6, 4, 2, 0, 2, 4, 6, 1000]

        static_obs_1 = [66.9928, 50.4973, 10, 649] # [x, y, lane, closest index]
        static_obs_2 = [70.6899, 61.4106, 6, 762]
        static_obs_3 = [80.1545, 77.3181, 8, 948]
        obs_list = [static_obs_1, static_obs_2, static_obs_3] 
        for obs in obs_list:
            if obs[3]+3<self.shared.ego.index:
                continue
            if static_obs_3[3]+10 < self.shared.ego.index:
                # print("all static obstacle passed")
                break
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)
            term = distance**1.3
            obs_value = [50/term, 100/term, 200/term, 100/term, 50/term]

            if obs[2]-2>=0:
                path_weight[obs[2]-2] += obs_value[0]
            if obs[2]-1>=0:
                path_weight[obs[2]-1] += obs_value[1]
            path_weight[obs[2]] += obs_value[2]
            if obs[2]+1<=len(path_weight):
                path_weight[obs[2]+1] += obs_value[3]
            if obs[2]+2<=len(path_weight):
                path_weight[obs[2]+2] += obs_value[4]
            

        # obs_1_start = [97.01, 104.32, 10, 1266] # x, y, lane, index
        # obs_1_middle_1 = [93.91, 103.9, 8, 1248]
        obs_1_middle_2 = [92.57, 103.58, 9, 1239]
        obs_1_end = [89.18, 103.03, 7, 1219]
        # obs_1_list = [obs_1_start, obs_1_middle_1, obs_1_middle_2, obs_1_end] # lane별로 늘려서
        obs_1_list = [obs_1_middle_2, obs_1_end] # lane별로 늘려서
        gain = 0.3
        for obs in obs_1_list:
            if obs_1_end[3]+10 < self.shared.ego.index:
                break
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)
            if distance > 15:
                continue
            # print("distance : ", distance)
            obs_value = [100/(distance**0.5)*gain, 200/(distance**0.5)*gain, 100/(distance**0.5)*gain] # gain 3->5
            if 0<obs[2]<len(path_weight):
                # print(obs_value)
                path_weight[obs[2]-1] += obs_value[0]
                path_weight[obs[2]] += obs_value[1]
                path_weight[obs[2]+1] += obs_value[2] 
            
            gain += 0.2

        # obs_2_start = [104.55, 130.04, 4, 1530] # x, y, lane, index
        # obs_2_middle_1 = [106.33, 129.30, 6, 1532]
        obs_2_middle_2 = [107.22, 128.74, 8, 1531]
        obs_2_end = [108.84, 127.63, 10, 1529]
        # obs_2_list = [obs_2_start, obs_2_middle_1, obs_2_middle_2, obs_2_end] # lane별로 늘려서
        obs_2_list = [obs_2_middle_2, obs_2_end] # lane별로 늘려서
        gain = 0.3
        for obs in obs_2_list:
            if obs_2_end[3]+10 < self.shared.ego.index:
                break
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)
            if distance > 15:
                continue
            # print("distance : ", distance)
            term = distance**1.3
            obs_value = [50/term, 100/term, 200/term, 100/term, 50/term]

            # obs_value = [100/(distance**0.5)*gain, 200/(distance**0.5)*gain, 100/(distance**0.5)*gain] # gain 3->5
            if 0<obs[2]<len(path_weight):
                # print(obs_value)
                path_weight[obs[2]-1] += obs_value[0]
                path_weight[obs[2]] += obs_value[1]
                path_weight[obs[2]+1] += obs_value[2] 

            gain += 0.1

        # obs_3_start = [104.55, 130.04, 4, 1530] # x, y, lane, index
        # obs_3_middle_1 = [106.33, 129.30, 6, 1532]
        obs_3_middle_2 = [90.06, 173.13, 7, 2175]
        obs_3_end = [91.98, 173.69, 9, 2162]
        # obs_3_list = [obs_3_start, obs_3_middle_1, obs_3_middle_2, obs_3_end] # lane별로 늘려서
        obs_3_list = [obs_3_middle_2, obs_3_end] # lane별로 늘려서
        gain = 0.3
        for obs in obs_3_list:
            if obs_3_end[3]+10 < self.shared.ego.index:
                break
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)
            if distance > 15:
                continue
            # print("distance : ", distance)
            term = distance**1.3
            obs_value = [50/term, 100/term, 200/term, 100/term, 50/term]

            # obs_value = [100/(distance**0.5)*gain, 200/(distance**0.5)*gain, 100/(distance**0.5)*gain] # gain 3->5
            if 0<obs[2]<len(path_weight):
                # print(obs_value)
                path_weight[obs[2]-1] += obs_value[0]
                path_weight[obs[2]] += obs_value[1]
                path_weight[obs[2]+1] += obs_value[2] 

            gain += 0.1

        # obs_3_start = [104.55, 130.04, 4, 1530] # x, y, lane, index
        # obs_3_middle_1 = [106.33, 129.30, 6, 1532]
        obs_4_middle_2 = [77.20, 180.35, 8, 2323]
        obs_4_end = [79.41, 179.05, 6, 2301]
        # obs_4_list = [obs_4_start, obs_4_middle_1, obs_4_middle_2, obs_4_end] # lane별로 늘려서
        obs_4_list = [obs_4_middle_2, obs_4_end] # lane별로 늘려서
        gain = 0.3
        for obs in obs_4_list:
            if obs_4_end[3]+10 < self.shared.ego.index:
                break
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)
            if distance > 15:
                continue
            # print("distance : ", distance)
            term = distance**1.3
            obs_value = [50/term, 100/term, 200/term, 100/term, 50/term]

            # obs_value = [100/(distance**0.5)*gain, 200/(distance**0.5)*gain, 100/(distance**0.5)*gain] # gain 3->5
            if 0<obs[2]<len(path_weight):
                # print(obs_value)
                path_weight[obs[2]-1] += obs_value[0]
                path_weight[obs[2]] += obs_value[1]
                path_weight[obs[2]+1] += obs_value[2] 

            gain += 0.1


        print("Weight :", list(np.round(path_weight, 1)))
        

        # print("ego index : ", self.shared.ego.index)
        # print(self.shared.ego.x)
        # print(self.shared.ego.y)
        return path_weight

    def path_maker(self):
        lattice = []
        
        look_distance = int(self.ego.speed * 2)

        # look distance
        if look_distance < 2 :
            look_distance = 2
        if look_distance > 10 :
            look_distance = 10

        look_distance = 35

        # 변환행렬
        if len(self.cut_path.x) > look_distance :
            global_ref_start_point = (self.cut_path.x[0], self.cut_path.y[0])
            global_ref_start_next_point = (self.cut_path.x[1], self.cut_path.y[1])
            global_ref_end_point = (self.cut_path.x[look_distance], self.cut_path.y[look_distance])
            
            theta = atan2(global_ref_start_next_point[1]-global_ref_start_point[1], global_ref_start_next_point[0]-global_ref_start_point[0])
            translation = [global_ref_start_point[0], global_ref_start_point[1]]

            t = np.array([[cos(theta), -sin(theta), translation[0]], [sin(theta), cos(theta), translation[1]], [0,0,1]])
            det_t = np.array([[t[0][0], t[1][0], -(t[0][0] * translation[0] + t[1][0] * translation[1])], [t[0][1], t[1][1], -(t[0][1] * translation[0] + t[1][1] * translation[1])], [0,0,1]])

            world_end_point = np.array([[global_ref_end_point[0]], [global_ref_end_point[1]], [1]])
            local_end_point = det_t.dot(world_end_point)
            world_current_point = np.array([[self.ego.x], [self.ego.y], [1]])
            local_current_point = det_t.dot(world_current_point)

            # self.lane_offset = [3.5, 0, -3.5, -4]
            # self.lane_offset = [5.5, 3.5, 1.1, 0, -1.1, -2.2, -3.3]
            local_lattice_points = []
            for i in range(len(self.lane_offset)):
                local_lattice_points.append([local_end_point[0][0], local_end_point[1][0] + self.lane_offset[i], 1])

            for end_point in local_lattice_points:
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

                sub_lattice_path = Path()

                for i in range(0, len(y)):
                    local_result = np.array([[x[i]], [y[i]], [1]])
                    global_result = t.dot(local_result)

                    tmp_x = global_result[0][0]
                    tmp_y = global_result[1][0]

                    sub_lattice_path.x.append(tmp_x)
                    sub_lattice_path.y.append(tmp_y)

                lattice.append(sub_lattice_path)
            
            add_point_size = int(self.ego.speed * 4)
            
            add_point_size = 100

            if add_point_size > len(self.cut_path.x) - 2:
                add_point_size = len(self.cut_path.x)

            elif add_point_size < 5 :
                add_point_size = 5
            
            for i in range(look_distance, add_point_size):
                if i + 1 < len(self.cut_path.x):
                    tmp_theta = atan2(self.cut_path.y[i+1] - self.cut_path.y[i], self.cut_path.x[i+1] - self.cut_path.x[i])
                    
                    tmp_translation = [self.cut_path.x[i], self.cut_path.y[i]]
                    tmp_t = np.array([[cos(tmp_theta), -sin(tmp_theta), tmp_translation[0]], [sin(tmp_theta), cos(tmp_theta), tmp_translation[1]], [0,0,1]])

                    for lane_num in range(len(self.lane_offset)):
                        local_result = np.array([[0], [self.lane_offset[lane_num]], [1]])
                        global_result = tmp_t.dot(local_result)

                        tmp_x = global_result[0][0]
                        tmp_y = global_result[1][0]
                        lattice[lane_num].x.append(tmp_x)
                        lattice[lane_num].y.append(tmp_y)

        if len(self.lattice_path) == 0:
            for i in range(len(self.lane_offset)):
                self.lattice_path.append(lattice[i])
        else:
            for i in range(len(self.lane_offset)):
                self.lattice_path[i] = lattice[i]