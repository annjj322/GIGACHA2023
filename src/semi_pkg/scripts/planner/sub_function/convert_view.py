#! /usr/bin/python3
# -*- coding: utf-8 -*-
from numpy import dot, sin, cos, radians, sqrt, round
import matplotlib.pyplot as plt

def scale(vec, origin=[0,0]):
    return sqrt((vec[0]-origin[0])**2 + (vec[1]-origin[1])**2)

def convert_coord(angle, vec, offset=[0,0]):
    angle = radians(angle)
    R = [[cos(angle), -sin(angle)],
         [sin(angle), cos(angle)]]

    rotated = dot(R, vec)
    converted = rotated+offset
    return converted

if __name__ == "__main__":
    angle = 270
    cam_left = [-0.45, 1.48]
    cam_right = [0.27, 1.96]
    offset=[0.47,0.695]
    real_l = [offset[0]+1.5, offset[1]+0.5]
    real_r = [offset[0]+2.0, offset[1]-0.3]
    l = convert_coord(angle, cam_left, offset)
    r = convert_coord(angle, cam_right, offset)
    print("left_x error :", round((real_l[0]-l[0])/real_l[0]*100, 3))
    print("left_y error :", round((real_l[1]-l[1])/real_l[1]*100, 3))
    print("right_x error :", round((real_r[0]-r[0])/real_r[0]*100, 3))
    print("right_y error :", round((real_r[1]-r[1])/real_r[1]*100, 3))


    # plot points
    plt.plot([0], [0], 'ro', label='origin')
    plt.plot(l[0], l[1], 'yo', label='cam_points')
    plt.plot(r[0], r[1], 'yo')
    plt.plot([offset[0],l[0]], [offset[1],l[1]], 'y-')
    plt.plot([offset[0],r[0]], [offset[1],r[1]], 'y-')
    plt.plot(real_l[0], real_l[1], "go", label='real_points')
    plt.plot(real_r[0], real_r[1], "go")

    # plot cam, xy_planes
    plt.plot([0,offset[0]], [0,offset[1]], '-', label="cam_offset")
    plt.plot([offset[0]], [offset[1]], 'bo')
    plt.plot([offset[0], offset[0]+convert_coord(angle, [1,0])[0]/2], [offset[1], offset[1]+convert_coord(angle, [1,0])[1]/2], "b-", label="cam_view_xy")
    plt.plot([offset[0], offset[0]+convert_coord(angle, [0,1])[0]/2], [offset[1], offset[1]+convert_coord(angle, [0,1])[1]/2], "b-")
    plt.plot([0, 1/2], [0, 0], "r-", label="ego_xy")
    plt.plot([0, 0], [0, 1/2], "r-")

    # show
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.legend()
    plt.grid()
    plt.show()