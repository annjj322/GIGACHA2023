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

        self.lane_weight = np.array([1000, 1000, 1000, 1000, 1000, 1000, 0])
        self.isObstacle = np.array([1000, 1000, 1000, 1000])
        self.min_val = 0
        self.check = 0

    def select_trajectory(self):
        self.shared.selected_lane = self.lane_weight.index(min(self.lane_weight))

    def weight_function_AEB(self):  #!! AEB's weight function !!
        self.isObstacle = np.array([1000, 1000, 1000, 1000])

        for i in range(len(self.isObstacle)): # 0,1,2
            path_check = True
            if path_check == True:
                self.shared.perception.lidar_lock.acquire()
                for j in range(len(self.lattice_path[i].x)): # paths' index
                    if path_check == False:
                        break
                    for k in range(len(self.shared.perception.objx)): # of obj
                        ob_point_distance = sqrt((self.lattice_path[i].x[j] - self.shared.perception.objx[k])**2 + (self.lattice_path[i].y[j] - self.shared.perception.objy[k])**2)
                        if ob_point_distance < (self.shared.perception.objw[k]/2+1): #and self.Obstacle_in_section == 0:
                            self.isObstacle[i] = j # not 1000
                            path_check = False
                            break
                        else:
                            self.isObstacle[i] = 1000
                self.shared.perception.lidar_lock.release()

        if self.isObstacle[2] != 1000:
            self.shared.plan.obstac = True
            self.lane_weight = np.array([1000, 1000, 0, 1000])
        else:
            self.shared.plan.obstac = False

            # if(self.isObstacle[2] < self.isObstacle[0]):
            #     print("+++++++++++++\nobstacle in lane 1\n++++++++++++")
            #     self.lane_weight = [0, 1000, 1000, 1000]
        # elif (self.shared.selected_lane == 0 and self.isObstacle[0] != 1000):
        #     if(self.isObstacle[0] > self.isObstacle[2]):
        #         print("+++++++++++++\nobstacle in lane 2\n++++++++++++")
        #         self.lane_weight = [1000, 1000, 0, 1000]
        # elif (self.shared.selected_lane == 0 and self.isObstacle[0] == 1000):
        #     if(self.isObstacle[2] != 1000):
        #         print("+++++++++++++\nobstacle in lane 2\n++++++++++++")
        #         self.lane_weight = [0, 1000, 1000, 1000]
        #     else:
        #         self.lane_weight = [1000, 1000, 0, 1000]
        


    def weight_function_obstacle_avoidance(self):
        self.isObstacle = np.array([1000, 1000, 1000, 1000])

        for i in range(len(self.isObstacle)): # 0,1,2
            path_check = True
            if path_check == True:
                self.shared.perception.lidar_lock.acquire()
                for j in range(len(self.lattice_path[i].x)): # paths' index
                    if path_check == False:
                        break
                    for k in range(len(self.shared.perception.objx)): # of obj
                        ob_point_distance = sqrt((self.lattice_path[i].x[j] - self.shared.perception.objx[k])**2 + (self.lattice_path[i].y[j] - self.shared.perception.objy[k])**2)
                        if ob_point_distance < (self.shared.perception.objw[k]/2+1): #and self.Obstacle_in_section == 0:
                            self.isObstacle[i] = j
                            path_check = False
                            break
                        else:
                            self.isObstacle[i] = 1000
                self.min_val = min(self.isObstacle)
                self.check = abs(self.isObstacle[3]- self.isObstacle[1])
                self.shared.perception.lidar_lock.release()

        if ((self.isObstacle[3] != 1000 and self.isObstacle[2] != 1000 and self.isObstacle[1] != 1000) and self.check <= 10):
            #if((self.isObstacle[2] == self.min_val or self.isObstacle[3] == self.min_val) and self.check <= 10): 
                # print("+++++++++++++\nobstacle in lane 1,2,3\n++++++++++++")
            self.lane_weight = np.array([0,1000,1000,1000])
        
        elif ((self.isObstacle[1] != 1000 and self.isObstacle[2] != 1000) or (self.isObstacle[1] != 1000)):
            if(self.isObstacle[1] == self.min_val or self.isObstacle[2] == self.min_val): 
                # print("+++++++++++++\nobstacle in lane 1 and 2 or 1\n++++++++++++")
                self.lane_weight = np.array([1000,1000,1000, 0])
        
        elif ((self.isObstacle[3] != 1000 and self.isObstacle[2] != 1000) or (self.isObstacle[3] != 1000)):
            if(self.isObstacle[2] == self.min_val or self.isObstacle[3] == self.min_val): 
                # print("+++++++++++++\nobstacle in lane 2 and 3 or 3\n++++++++++++")
                self.lane_weight = np.array([0,1000,1000,1000])

        elif (self.isObstacle[2] != 1000):
            if(self.isObstacle[2] == self.min_val): 
                # print("+++++++++++++\nobstacle in only 2\n++++++++++++")
                self.lane_weight = np.array([0,1000,1000,1000])

        elif (self.isObstacle[3] == 1000 and self.isObstacle[2] == 1000 and self.isObstacle[1] == 1000):
            # print("+++++++++++++\nNo obstacle in lane\n++++++++++++")
            self.lane_weight = np.array([1000,1000,0,1000])

    def path_maker(self):
        lattice = np.array([])
        
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
            translation = np.array([global_ref_start_point[0], global_ref_start_point[1]])

            t = np.array([[cos(theta), -sin(theta), translation[0]], [sin(theta), cos(theta), translation[1]], [0,0,1]])
            det_t = np.array([[t[0][0], t[1][0], -(t[0][0] * translation[0] + t[1][0] * translation[1])], [t[0][1], t[1][1], -(t[0][1] * translation[0] + t[1][1] * translation[1])], [0,0,1]])

            world_end_point = np.array([[global_ref_end_point[0]], [global_ref_end_point[1]], [1]])
            local_end_point = det_t.dot(world_end_point)
            world_current_point = np.array([[self.ego.x], [self.ego.y], [1]])
            local_current_point = det_t.dot(world_current_point)

            # lane_off_set = [3.5, 0, -3.5, -4]
            lane_off_set = np.array([5.5, 3.5, 1.1, 0, -1.1, -2.2, -3.3])

            local_lattice_points = []
            for i in range(len(lane_off_set)):
                local_lattice_points.append([local_end_point[0][0], local_end_point[1][0] + lane_off_set[i], 1])

            for end_point in local_lattice_points:
                x = np.array([])
                y = np.array([])
                x_interval = 0.5
                xs = 0
                xf = end_point[0]
                ps = local_current_point[1][0]

                pf = end_point[1]
                x_num = xf / x_interval

                for i in range(xs, int(x_num)): 
                    x.append(i * x_interval)
                
                a = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
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

                    for lane_num in range(len(lane_off_set)):
                        local_result = np.array([[0], [lane_off_set[lane_num]], [1]])
                        global_result = tmp_t.dot(local_result)

                        tmp_x = global_result[0][0]
                        tmp_y = global_result[1][0]
                        lattice[lane_num].x.append(tmp_x)
                        lattice[lane_num].y.append(tmp_y)

        if len(self.lattice_path) == 0:
            for i in range(len(lane_off_set)):
                self.lattice_path.append(lattice[i])
        else:
            for i in range(len(lane_off_set)):
                self.lattice_path[i] = lattice[i]