import pymap3d

#Songdo
# base_lat = 37.3843177
# base_lon = 126.6553022
# base_alt = 15.4

#simul_kcity_sangwook
base_lat = 37.2389871166175 
base_lon = 126.772996046328
base_alt = 15.4

#Songdo ParkingLot
# parking_lat = 37.3848150059503
# parking_lon = 126.655830146935

#simul_kcity_sangwook ParkingLot
parking_lat = 37.2392303963579
parking_lon = 126.773196841119

# parking_lat = 37.2392083231717
# parking_lon = 126.773241462183

def parking_call_back():
        x, y, _ = pymap3d.geodetic2enu(parking_lat, parking_lon, base_alt, \
                                            base_lat, base_lon, base_alt)
        return x,y