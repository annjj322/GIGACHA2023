from planner_and_control.msg import Path
from math import cos, degrees, radians, sin, atan2, sqrt
from lib.local_utils.enu import parking_call_back
from numpy import rad2deg

WB = 1.04
max_angle = 27
kingpin_r = 0.05
minimum_radius = WB/sin(radians(max_angle)) + kingpin_r
smooth_radius = 5

# 여기서 parking_lot은 주차 구역 입구 정중앙을 뜻함.


def findParkingPath(path, ego):
    global heading
    min_index = 0
    min_dis = 10000000
    forward_path = Path()
    backward_path = Path()

    parking_x, parking_y = parking_call_back()

    parking_lot = {
        'x': parking_x,
        'y': parking_y
    }

    ######### 주차점과 가장 가까운 path 점 찾기 ########
    for i in range(len(path.x)):
        dx = parking_lot['x'] - path.x[i]
        dy = parking_lot['y'] - path.y[i]
        dis = sqrt(dx*dx + dy*dy)
        if dis < min_dis:
            min_dis = dis
            min_index = i
    print(f"min_inex : {min_index}")
    heading = rad2deg(atan2(
        (path.y[min_index]-path.y[min_index - 1]), (path.x[min_index]-path.x[min_index - 1])))
    print(f"yaw : {heading}")

    ######### O2, O1 원점 찾기 ########
    O2_x, O2_y = find_O2(path, ego, min_index)
    O1_x, O1_y, heading_O1_02, dis_O1_to_lot = find_O1(
        path, ego, min_index, parking_lot)

    O3_x, O3_y, theta_O3_to_lot = find_O3(
        path, ego, min_index, parking_lot, heading)

    ######### 전진 원호 생성 ########
    forward_path = make_arc_path(
        O2_x, O2_y, heading - 90, heading + 180, minimum_radius, forward_path, 1)  # 지금 이건 360도 기준으로 계산함

    # forward_path = make_arc_path(O3_x, O3_y, heading+ 90, heading+90-theta_O3_to_lot, smooth_radius, forward_path, -1) # smooth 전진 원호

    ######### 후진 원호 생성 ########
    O2_back_arc_heading = heading - (90 - heading_O1_02)

    backward_path = make_arc_path(
        O2_x, O2_y, heading, O2_back_arc_heading, minimum_radius, backward_path, -1)

    backward_path = make_arc_path(
        O1_x, O1_y, O2_back_arc_heading+180, heading + 180, dis_O1_to_lot, backward_path, 1)  # 지금 이건 360도 기준으로 계산함

    print("Parking_path Created")

    return forward_path, backward_path


def find_O2(path, ego, min_index):

    # distance_from_min_index
    dis_mindex = sqrt((path.x[ego.index] - path.x[min_index])
                      ** 2 + (path.y[ego.index] - path.y[min_index])**2)  # 차량과  주차점 가장 근처 path 사이 직선 거리

    dis_O2 = sqrt((dis_mindex)**2 + minimum_radius**2)  # O2와 차량 사이 거리

    theta_O2_mindex = rad2deg(atan2(minimum_radius / dis_mindex, 1.0))
    heading_to_O2 = heading + theta_O2_mindex  # heading 음수일 때는 달라짐

    O2_x = path.x[ego.index] + dis_O2*cos(radians(heading_to_O2))
    O2_y = path.y[ego.index] + dis_O2*sin(radians(heading_to_O2))

    return O2_x, O2_y


def find_O1(path, ego, min_index, parking_lot):

    dis_mindex_to_lot = sqrt((parking_lot['x'] - path.x[min_index])**2 + (
        parking_lot['y'] - path.y[min_index])**2)  # mindex와 parking_lot 사이 거리

    dis_O1_to_lot = dis_mindex_to_lot * \
        (1+dis_mindex_to_lot/(2*minimum_radius))  # O1과 parking_lot사이 수직 거리

    O1_x = parking_lot['x'] + dis_O1_to_lot*cos(radians(heading))
    O1_y = parking_lot['y'] + dis_O1_to_lot*sin(radians(heading))

    theta_O1_to_O2 = rad2deg(atan2(
        dis_O1_to_lot / (dis_mindex_to_lot + minimum_radius), 1.0))

    return O1_x, O1_y, theta_O1_to_O2, dis_O1_to_lot


def find_O3(path, ego, min_index, parking_lot, heading):

    dis_mindex_to_lot = sqrt((parking_lot['x'] - path.x[min_index])**2 + (
        parking_lot['y'] - path.y[min_index])**2)
    dis_mindex_to_start = sqrt(2*dis_mindex_to_lot *
                               smooth_radius - dis_mindex_to_lot**2)
    dis_mindex_to_ego = sqrt((path.x[min_index]-path.x[ego.index])
                             ** 2 + (path.y[min_index]-path.y[ego.index])**2)
    dis_start_to_ego = dis_mindex_to_ego - dis_mindex_to_start
    dis_O3 = sqrt(smooth_radius**2 + dis_start_to_ego**2)

    theta_O3 = rad2deg(
        atan2(smooth_radius/dis_start_to_ego, 1))
    heading_to_O3 = heading - theta_O3

    theta_O3_to_lot = rad2deg(
        atan2(dis_mindex_to_start/(smooth_radius-dis_mindex_to_lot), 1))

    O3_x = path.x[ego.index] + dis_O3*cos(radians(heading_to_O3))
    O3_y = path.y[ego.index] + dis_O3*sin(radians(heading_to_O3))

    return O3_x, O3_y, theta_O3_to_lot


def make_arc_path(x, y, start, end, radius, path, direction):
    start = int(round(start))
    end = int(round(end))

    for theta in range(start, end, direction):
        path.x.append(x+radius*cos(radians(theta)))
        path.y.append(y+radius*sin(radians(theta)))

    return path
