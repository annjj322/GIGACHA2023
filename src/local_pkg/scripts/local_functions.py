import math
import numpy as np

def euler_from_quaternion(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z # in radians

def circumradius(xvals, yvals):
    x1, x2, x3, y1, y2, y3 = xvals[0], xvals[1], xvals[2],\
    yvals[0], yvals[1], yvals[2]

    den = 2 * ((x2-x1) * (y3-y2)-(y2-y1) * (x3-x2))
    num = ( (((x2-x1)**2) + ((y2-y1)**2)) * (((x3-x2)**2) + ((y3-y2)**2)) * (((x1-x3)**2) + ((y1-y3)**2)) )**0.5

    if den == 0:
        return 0
    
    r = abs(num/den)

    return r

def low_pass_filter(data, size, alpha):
    meas = []
    meas.append(data)
    mean = np.mean(meas)

    if len(meas) > size:
        meas.pop(0)
        mean = np.mean(meas)

    filter_mean = alpha * mean + (1-alpha) * meas[-1]

    return filter_mean

def quaternion_from_euler(roll, pitch, yaw):

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return qx, qy, qz, qw