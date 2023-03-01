from math import sqrt

def findLocalPath(path, ego, cut_path):
    if ego.index + 100 > len(path.x):
        last_local_index = len(path.x)
    else:
        last_local_index = ego.index + 100

    if len(cut_path.x) == 0:
        for i in range(ego.index, last_local_index):
            cut_path.x.append(path.x[i])
            cut_path.y.append(path.y[i])
    else:
        count = 0
        for i in range(ego.index, last_local_index):
            cut_path.x[count] = path.x[i]
            cut_path.y[count] = path.y[i]
            count += 1