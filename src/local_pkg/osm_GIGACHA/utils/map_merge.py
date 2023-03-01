import json


files=['final_map.json', 'final_path5.json']

def merge_JsonFiles(filename):
    data_dict = dict()
    data_list = []
    for f1 in filename:
        with open(f1, 'r') as infile:
            data = json.load(infile)
            data_list.extend(data.values())

    for n, nodes in enumerate(data_list):
        data_dict[n] = nodes
    
    j = json.dumps(data_dict, indent = 4)
    f = open('final_path.json', 'w')
    print(j, file = f)
    f.close()

merge_JsonFiles(files)