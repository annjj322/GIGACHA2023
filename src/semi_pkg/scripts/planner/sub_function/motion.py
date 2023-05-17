from math import sqrt
from math import sqrt
from math import cos,sin,atan2,atan
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

        # self.lane_offset = [5.4, 4.35, 3.3, 2.75, 2.2, 1.7, 1.2, 0.2, 0, -0.25, -0.7, -1.45, -2.2] # for kcity map # 원래 장애물 회피를 위한 오프셋임. 0인 lane이 없어서 주차 때는 아래를 사용
        self.lane_offset = [0]
        self.lane_weight = None

        
    def select_trajectory(self):
        # for obs avoidance
        self.shared.selected_lane = self.lane_weight.index(min(self.lane_weight))

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

    def obs_lane(self, cx, cy):
        distance = []
        for lane in self.shared.lattice_path:
            dx = [cx - x for x in lane.x[0 : -1]]
            dy = [cy - y for y in lane.y[0 : -1]]
            dist = np.hypot(dx, dy)
            np_dist = np.array(dist)
            distance.append(np.min(np_dist))
        
        lane_num = int(np.argmin(distance))

        return lane_num

    def obs_nearest_index(self, cx, cy):

        dx = [cx - x for x in self.global_path.x[0 : -1]]
        dy = [cy - y for y in self.global_path.y[0 : -1]]
        dist = np.hypot(dx, dy)

        index = int(np.argmin(dist))

        return index

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

        l = ((self.L + self.shared.perception.rx)**2 + (self.shared.perception.ry)**2)**0.5
        cx = self.shared.ego.x + l*cos(np.radians(self.shared.ego.heading) - atan(self.ry/(self.rx + self.L))) # 이게 중요
        cy = self.shared.ego.y + l*sin(np.radians(self.shared.ego.heading) - atan(self.ry/(self.rx + self.L))) # 이게 중요
        obs_ind = self.obs_nearest_index(cx, cy)
        lane_num = self.obs_lane(cx, cy)
        obs_predict_1 = [cx, cy, lane_num, obs_ind]
        obs_predict_2 = [cx, cy, lane_num, obs_ind]

        obs_list = [obs_predict_1, obs_predict_2] # lane별로 늘려서
        gain = 0.3

        for obs in obs_list:
            # 1m 이상 지났을 경우 반영 중단
            if obs_predict_2[3]+10 < self.shared.ego.index: 
                break

            # 장애물 거리 측정
            distance = sqrt((self.shared.ego.x-obs[0])**2+(self.shared.ego.y-obs[1])**2)

            # 15m 이상 떨어져 있을 경우 무시
            if distance > 15:
                continue
            
            # weight 반영
            term = distance**1.3 # 실험적 값
            obs_value = [50/term, 100/term, 200/term, 100/term, 50/term]
            if 0<obs[2]<len(path_weight):
                path_weight[obs[2]-1] += obs_value[0]
                path_weight[obs[2]] += obs_value[1]
                path_weight[obs[2]+1] += obs_value[2] 
            gain += 0.1


        print("Weight : ", list(np.round(path_weight, 1)))
        return path_weight

   