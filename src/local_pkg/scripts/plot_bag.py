import matplotlib.pyplot as plt
import pandas as pd

csv_file = '1.csv'
data_frame = pd.read_csv(csv_file)

x = data_frame['x']
y = data_frame['y']
#time = data_frame['time']
#heading = data_frame['heading']
#gps_heading = data_frame['gps_heading']
#speed = data_frame['speeed']
#gspeed = data_frame['gspeed']
#gear = data_frame['gear']
#headAcc = data_frame['headAcc']

plt.figure()

plt.plot(x,y)
#plt.plot(time,heading,label='heading')
#plt.plot(time,gps_heading,label='gps_heading')
#plt.plot(time,speed,label='speeed')
#plt.plot(time,gspeed,label='gspeed')
#plt.plot(time,gear,label='gear')
#plt.plot(time,gear,label='headAcc')

plt.xlabel('x')
plt.ylabel('y')
plt.title('local msg')

plt.legend()

plt.show()

