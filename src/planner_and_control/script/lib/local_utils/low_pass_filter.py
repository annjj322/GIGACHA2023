import numpy as np

def low_pass_filter(data, size, alpha):

    meas = []
    mean = 0

    meas.append(data)
    mean = np.mean(meas)

    if len(meas) > size:
        meas.pop(0)
        mean = np.mean(meas)

    filter_mean = alpha * mean + (1-alpha) * meas[-1]

    return filter_mean