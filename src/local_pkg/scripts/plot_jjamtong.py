import json
import matplotlib.pyplot as plt
global_path_x = []
global_path_y =[]
with open(f"/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/Inha_Songdo/right_curve.json", 'r') as json_file:
    json_data = json.load(json_file)
    for _, (x, y, _, _) in enumerate(json_data.values()):
        global_path_x.append(x)
        global_path_y.append(y)
# plt.plot(global_path_x, global_path_y)
plt.plot(global_path_x, global_path_y, 'ro', ms=1)
plt.show()