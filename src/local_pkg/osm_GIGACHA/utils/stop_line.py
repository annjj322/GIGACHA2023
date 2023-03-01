import json
import numpy as np

with open('stop_line.json') as data:
    stop_data = json.load(data)

stop_line_ids = dict()
stop_line_data = dict()

central_data = dict()

x_list = dict()
y_list = dict()

for n, index in enumerate(stop_data):
    stop_line_ids[n] = list(stop_data['{}'.format(n)].keys())
    stop_line_data[n] = list(stop_data['{}'.format(n)].values())


for i in range(len(stop_line_data)):
    x_list[i] = []
    y_list[i] = []

    for i_ in range(len(stop_line_data[i])):
        x_list[i].append(stop_line_data[i][i_][0])
        y_list[i].append(stop_line_data[i][i_][1])

for i in range(len(x_list)):
    x_list[i] = (sum(x_list[i]) / len(x_list[i]))
    y_list[i] = (sum(y_list[i]) / len(y_list[i]))


for i in range(len(x_list)):
    central_data[i] = []
    central_data[i].append(x_list[i])
    central_data[i].append(y_list[i])

j = json.dumps(central_data, indent = 4)
f = open('stop_line_coordinates.json', 'w')
print(j, file = f)
f.close()