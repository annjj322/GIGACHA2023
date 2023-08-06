import numpy as np

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
    
    # 척력장 계산
    def calculate_repulsive_field(self):
        repulsive = 0
        repulsive_scale = 0 
        for obstacle in self.obstacles:
            distance = np.linalg.norm(self.vehicle_position - obstacle)
            distance += 0.01
            ###
            scale = 1/distance+1
            ###

            unit_vector = (self.vehicle_position - obstacle)/distance**3

            repulsive += unit_vector * scale
            repulsive_scale += scale
        return repulsive, repulsive_scale
    
    def calculate_attractive_field(self):
        self.attractive = 0
        distance = np.linalg.norm(self.vehicle_position - self.goal_position)

        ###
        scale = 8/distance
        ###

        unit_vector = (goal_position - self.vehicle_position)/distance

        attractive = unit_vector * scale
        attractive_scale = scale

        return attractive, attractive_scale
    
    def calculate_potential_field(self, repulsive, repulsive_scale, attractive, attractive_scale):
        self.potential = repulsive + attractive

        # for erp42 : constant speed
        self.potential = self.potential/np.linalg.norm(self.potential)
        scale = 0.3
        self.potential = self.potential*scale

        self.potential_scale = repulsive_scale + attractive_scale

        

    def run(self, plot=False):
        # self.update(vehicle_position, goal_position, obstacles)
        repulsive, rep_scale = self.calculate_repulsive_field()
        attractive, att_scale = self.calculate_attractive_field()
        self.calculate_potential_field(repulsive, rep_scale, attractive, att_scale)
        # if plot:
        #     self.plot()


    # def plot(self):
    #     plt.arrow(self.vehicle_position[0], self.vehicle_position[1], self.potential[0], self.potential[1],
    #                 head_width=0.1, head_length=0.1, fc='blue', ec='black')
    #     plt.xlim(0,10)
    #     plt.ylim(0,10)
    #     plt.scatter(self.obstacles[:, 0], self.obstacles[:, 1], color='red', label='Obstacles', marker='x', s=100)
    #     plt.scatter(self.goal_position[0], self.goal_position[1], color='green', label='Goal', marker='*', s=200)
    #     plt.title('Potential Field')
    #     plt.xlabel('X')
    #     plt.ylabel('Y')
    #     plt.legend()
    #     plt.grid()

if __name__ == "__main__":
    # 장애물과 목표지점의 위치 정의
    obstacles = ([[3.5,4], [4,4], [4.5,4], [5,4], \
                  [4.5,6], [5,6], [5.5,6], [6,6], [6.5,6]])
    for i in range(10):
        obstacles.append([3,i])
        obstacles.append([7,i])
    obstacles = np.array(obstacles)

    goal_position = np.array([5,9])
    start_location = np.array([3,5])
    
    # 객체 생성 및 초기화
    pf = Potential_field()
    vehicle_position = np.array([5,0])
    tmp_vehicle_position = vehicle_position.copy()
    actual_path = []

    # for recording
    # first = True
    # plt.figure(figsize=(8, 8))

    while 1:
        # plt.cla()
        actual_path = []
        pf.update(vehicle_position, goal_position, obstacles)
        tmp_vehicle_position = vehicle_position
        pf.run(plot=False)

        for i in range(100):
            if i == 10:
                vehicle_position = tmp_vehicle_position

            pf.update(tmp_vehicle_position, goal_position, obstacles)

            if tmp_vehicle_position[1]>9:
                break
            pf.run(plot=False)

            # update
            tmp_vehicle_position = tmp_vehicle_position + pf.potential/20
            goal_position = np.array([5, tmp_vehicle_position[1]+1.5])

            # plt.pause(0.0001)
            actual_path.append(list(tmp_vehicle_position))


    #     plt.xlim(0,10)
    #     plt.ylim(0,10)
    #     plt.scatter(pf.obstacles[:, 0], pf.obstacles[:, 1], color='red', label='Obstacles', marker='x', s=100)
    #     for point in actual_path:
    #         plt.plot(point[0], point[1], 'ro', markersize = 3)
    #     plt.plot(actual_path[-1][0], actual_path[-1][1], 'ro', label='Path', markersize = 3)
    #     plt.title('Potential Field')
    #     plt.xlabel('X')
    #     plt.ylabel('Y')
    #     plt.legend()
    #     plt.grid()
    #     plt.pause(0.0001)
    # plt.show()
