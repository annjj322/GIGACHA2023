import OSMHandler

lane_data = OSMHandler.OSM_data('B2_SURFACELINEMARK.osm')

left_change = [] #왼쪽으로만 차선 변경이 가능할 경우 right to left
right_change = [] #오른쪽으로만 차선 변경이 가능할 경우 left to right
both_change = [] #양쪽으로 차선 변경이 가능할 경우 

for data in lane_data:
    if data[0] == "way":
        if data[4]['Type'] == '224':
            try:
                print("===================")
                both_change.append((data[4]['L_linkID'], data[4]['R_linkID']))
            except KeyError:
                pass

# print(both_change)