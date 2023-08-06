import numpy as np
import matplotlib.pyplot as plt
from time import sleep
# class Potential_field:
#     def __init__(self):
#         self.repulsive = 0
#         self.attractive = 0
#         self.potential = 0

#         self.vehicle_position = None
#         self.goal_position = None
#         self.obstacles = None

#     def update(self, vehicle_position, goal_position, obstacles):
#         self.vehicle_position = vehicle_position
#         self.goal_position = goal_position
#         self.obstacles = obstacles
    
#     # 척력장 계산
#     def calculate_repulsive_field(self, vehicle_position, obstacles):
#         self.repulsive = 0    
#         for obstacle in obstacles:
#             distance = np.linalg.norm(vehicle_position - obstacle)
#             ###
#             scale = 1/distance+1
#             ###

#             unit_vector = (vehicle_position - obstacle)/distance**3

#             self.repulsive += unit_vector * scale
    
#     def calculate_attractive_field(self, vehicle_position, goal_position):
#         self.attractive = 0
        
#         distance = np.linalg.norm(vehicle_position - goal_position)

#         ###
#         scale = 8/distance
#         ###

#         unit_vector = (goal_position - vehicle_position)/distance

#         self.attractive = unit_vector * scale
#         # self.attractive[1]=0.5 * self.attractive[1]
    
#     def calculate_potential_field(self):
#         self.potential = self.repulsive + self.attractive

#         # for erp42 : constant speed
#         self.potential = self.potential/np.linalg.norm(self.potential)
#         scale = 0.3
#         self.potential = self.potential*scale

#     def run(self, vehicle_position, goal_position, obstacles, plot=False):
#         self.update(vehicle_position, goal_position, obstacles)
#         self.calculate_repulsive_field(self.vehicle_position, self.obstacles)
#         self.calculate_attractive_field(self.vehicle_position, self.goal_position)
#         self.calculate_potential_field()
#         if plot:
#             self.plot()
#         # print("Potential is ", self.potential)


#     def plot(self):
#         plt.arrow(vehicle_location[0], vehicle_location[1], self.potential[0], self.potential[1],
#                     head_width=0.1, head_length=0.1, fc='blue', ec='black')
#         plt.xlim(0,10)
#         plt.ylim(0,10)
#         plt.scatter(self.obstacles[:, 0], self.obstacles[:, 1], color='red', label='Obstacles', marker='x', s=100)
#         plt.scatter(self.goal_position[0], self.goal_position[1], color='green', label='Goal', marker='*', s=200)
#         plt.title('Potential Field')
#         plt.xlabel('X')
#         plt.ylabel('Y')
#         plt.legend()
#         plt.grid()

# if __name__ == "__main__":
#     # 장애물과 목표지점의 위치 정의
#     obstacles = ([[4.5,4], [4,4], [5,4], [5.5,6],[6.5,6], [6,6]])
#     for i in range(10):
#         obstacles.append([3,i])
#         obstacles.append([7,i])
#     obstacles = np.array(obstacles)

#     goal_position = np.array([5,9])
#     start_location = np.array([3,5])
    
#     # 2D 공간 정의
#     x_min, x_max = 0, 10
#     y_min, y_max = 0, 10
#     resolution = 1.0

#     x_range = np.arange(x_min, x_max, resolution)
#     y_range = np.arange(y_min, y_max, resolution)
#     X, Y = np.meshgrid(y_range, x_range)

#     pf = Potential_field()
    
#     pf.run(start_location, goal_position, obstacles)
#     vehicle_location = np.array([5,0])

#     path = []
    
#     # for recording
#     first = True
#     while 1:
#         if vehicle_location[1]>9:
#             break
#         plt.cla()
#         # pf.plot(vehicle_location)
#         pf.run(vehicle_location, goal_position, obstacles, plot=True)
#         vehicle_location = vehicle_location + pf.potential/5.0
#         goal_position = np.array([5, vehicle_location[1]+1.5])

#         print(pf.potential)
#         plt.pause(0.001)
#         path.append(list(vehicle_location))
#         if first:
#             sleep(3)
#             first = False
    
#     plt.show()
#     print(path)
#     plt.xlim(0,10)
#     plt.ylim(0,10)
#     plt.scatter(pf.obstacles[:, 0], pf.obstacles[:, 1], color='red', label='Obstacles', marker='x', s=100)
#     for point in path:
#         plt.plot(point[0], point[1], 'ro', markersize = 3)
#     plt.plot(path[-1][0], path[-1][1], 'ro', label='Path', markersize = 3)
#     plt.title('Potential Field')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.legend()
#     plt.grid()
#     plt.show()

class Potential_field:
    def __init__(self):
        self.repulsive = 0
        self.attractive = 0
        self.potential = 0

        self.vehicle_position = None
        self.goal_position = None
        self.obstacles = None

        # for visualization
        self.repulsive_scale = 0
        self.attractive_scale = 0
        self.potential_scale = 0

    def update(self, vehicle_position, goal_position, obstacles):
        self.repulsive = 0
        self.attractive = 0
        self.potential = 0

        self.vehicle_position = vehicle_position
        self.goal_position = goal_position
        self.obstacles = obstacles
    
    # ì²™ë ¥ìž¥ ê³„ì‚°
    def calculate_repulsive_field(self):
        self.repulsive = 0    
        for obstacle in self.obstacles:
            distance = np.linalg.norm(self.vehicle_position - obstacle)
            distance += 0.01

            ###
            scale = 1/distance**1.4 + 1
            ###

            unit_vector = (self.vehicle_position - obstacle)/distance**3

            self.repulsive += unit_vector * scale
            self.repulsive_scale += scale
    
    def calculate_attractive_field(self):
        self.attractive = 0
        distance = np.linalg.norm(self.vehicle_position - self.goal_position)

        ###
        scale = 7/distance**0.6
        ###

        unit_vector = (self.goal_position - self.vehicle_position)/distance

        self.attractive = unit_vector * scale
        self.attractive_scale = scale
    
    def calculate_potential_field(self):
        self.potential = self.repulsive + self.attractive

        # for erp42 : constant speed
        unit_vector = self.potential/np.linalg.norm(self.potential)
        scale = 0.3
        if self.potential[1] < 0:
            if self.potential[0] < 0:
                unit_vector = np.array([-1,0])
            else:
                unit_vector = np.array([1,0])


        self.potential = unit_vector*scale

        self.potential_scale = self.repulsive_scale + self.attractive_scale

            
        

    def run(self, plot=False):
        # self.update(vehicle_position, goal_position, obstacles)
        self.calculate_repulsive_field()
        self.calculate_attractive_field()
        self.calculate_potential_field()
        if plot:
            self.plot()


    def plot(self):
        plt.arrow(vehicle_position[0], vehicle_position[1], self.potential[0], self.potential[1],
                    head_width=0.1, head_length=0.1, fc='blue', ec='black')
        plt.xlim(0,10)
        plt.ylim(0,10)
        plt.scatter(self.obstacles[:, 0], self.obstacles[:, 1], color='red', label='Obstacles', marker='x', s=100)
        plt.scatter(self.goal_position[0], self.goal_position[1], color='green', label='Goal', marker='*', s=200)
        plt.title('Potential Field')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid()

if __name__ == "__main__":
    # ìž¥ì• ë¬¼ê³¼ ëª©í‘œì§€ì ì˜ ìœ„ì¹˜ ì •ì˜
    # obstacles = ([[3.5,4], [4,4], [4.5,4], [5,4], \
    #               [4.5,6], [5,6], [5.5,6], [6,6], [6.5,6]])

    obstacles = ([[3.5,4], [4,4], [4.5,4], [5,4], [6,6], [6.5,6]])

    val = 30
    for i in range(val):
        obstacles.append([3,i/(val/10)])
        obstacles.append([7,i/(val/10)])
    obstacles = np.array(obstacles)

    start_location = np.array([5,0])
    goal_position = np.array([5,1.5])
    
    # 2D ê³µê°„ ì •ì˜
    x_min, x_max = 0, 10
    y_min, y_max = 0, 10
    resolution = 0.1

    # ìž ìž¬ì ì¸ ìž¥ë ¥ ì‹œê°í™”
    x_range = np.arange(x_min, x_max, resolution)
    y_range = np.arange(y_min, y_max, resolution)
    X, Y = np.meshgrid(y_range, x_range)
    Z = np.zeros_like(X)
    
    
    pf = Potential_field()
    
    pf.update(start_location, goal_position, obstacles)
    pf.run()
    vehicle_position = np.array([5,0])

    path = []
    # for recording
    first = True
    plt.figure(figsize=(6, 6))

    last_obstacles = obstacles
    obs_flag = True
    while 1:

        if vehicle_position[1] > 4:
            if obs_flag:
                obstacles = list(obstacles)
                obstacles.extend([[4.5,6], [5,6], [5.5,6]])
                obstacles = np.array(obstacles)
            obs_flag = False

        # follower
        last_obstacles = obstacles
        if len(path) == 0:
            follower = vehicle_position - [0, 2]
        elif len(path) < 30:
            follower = path[0]
        else:
            follower = np.array(path[-30])
        obstacles = list(obstacles)
        obstacles.append(list(follower))
        obstacles = np.array(obstacles)
        

        # end point set
        if vehicle_position[1]>9:
            break

        # plot claer
        plt.cla()

        # run
        pf.update(vehicle_position, goal_position, obstacles)
        pf.run(plot=True)

        # update
        vehicle_position = vehicle_position + pf.potential/10
        if vehicle_position[1]+1.5 > goal_position[1]:
            goal_position = np.array([5, vehicle_position[1]+1.5])
        

        path.append(list(vehicle_position))


        tmp_vehicle_position = vehicle_position
        tmp_goal_position = goal_position
        actual_path = []
        for i in range(30):

            # update
            tmp_vehicle_position = tmp_vehicle_position + pf.potential/10
            tmp_goal_position = np.array([5, tmp_vehicle_position[1]+1.5])

            pf.update(tmp_vehicle_position, tmp_goal_position, obstacles)
            pf.run(plot=False)

            actual_path.append(list(tmp_vehicle_position))
            if first:
                first = False

        # follower
        obstacles = last_obstacles
        for point in actual_path[10:]:
            plt.plot(point[0], point[1], 'bo', markersize = 1)
        plt.pause(0.0001)

    plt.show()





    # plot last path
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.scatter(pf.obstacles[:, 0], pf.obstacles[:, 1], color='red', label='Obstacles', marker='x', s=100)
    for point in path:
        plt.plot(point[0], point[1], 'ro', markersize = 3)
        
    plt.plot(path[-1][0], path[-1][1], 'ro', label='Path', markersize = 3)
    plt.title('Potential Field')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid()
    plt.show()