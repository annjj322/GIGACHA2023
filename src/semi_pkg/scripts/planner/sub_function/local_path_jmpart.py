import numpy as np
import matplotlib.pyplot as plt

# 장애물과 목표지점의 위치 정의
obstacles = np.array([[2, 2], [4, 4], [5, 8], [7, 5], [8, 5]])
goal = np.array([9, 9])
start_location = np.array([3,5])

# 잠재적인 장력 계산 함수 정의
def calculate_potential_field(x, y):
    potential = 0
    
    for obstacle in obstacles:
        distance = np.linalg.norm([x - obstacle[0], y - obstacle[1]])
        potential += 1 / distance
    potential -= 1 / np.linalg.norm([x - goal[0], y - goal[1]])
    return potential

# 2D 공간 정의
x_min, x_max = 0, 10
y_min, y_max = 0, 10
resolution = 0.3

# 잠재적인 장력 시각화
x_range = np.arange(x_min, x_max, resolution)
y_range = np.arange(y_min, y_max, resolution)
X, Y = np.meshgrid(y_range, x_range)
Z = np.zeros_like(X)

for i in range(len(x_range)):
    for j in range(len(y_range)):
        Z[i, j] = calculate_potential_field(x_range[i], y_range[j])
        print(type(calculate_potential_field(x_range[i], y_range[j])))
print(Z)
# 그래프 그리기
plt.figure(figsize=(8, 8))
# plt.contourf(Y, X, Z, levels=20, cmap='plasma', alpha=0.8)
plt.contourf(Y, X, Z, levels=20, cmap='viridis', alpha=0.8)
plt.colorbar(label='Potential Field')
plt.scatter(obstacles[:, 0], obstacles[:, 1], color='red', label='Obstacles', marker='x', s=100)
plt.scatter(goal[0], goal[1], color='green', label='Goal', marker='*', s=200)
plt.plot(start_location[0], start_location[1])
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Potential Field')
plt.legend()
plt.grid()
plt.show()

    

