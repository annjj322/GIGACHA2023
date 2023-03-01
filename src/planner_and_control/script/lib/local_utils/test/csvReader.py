import matplotlib.pyplot as plt
import csv
import matplotlib.ticker as ticker
import numpy as np
x = []
imu = []
gps = []
f = open("data2Low.csv")
# append values to list
for row in csv.reader(f):
    x.append(row[0])
    imu.append(row[1])
    gps.append(row[2])

imu1=[]
gps1=[]
d = open("data2High.csv")
# append values to list
for row in csv.reader(d):
    imu1.append(row[1])
    gps1.append(row[2])

ref=[]
for i in range(100):
    ref.append(45)

# ax=plt.axes()
# ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(5))


plt.subplot(2, 1, 1)
plt.plot(x, imu, 'r.')
plt.plot(x, ref, color="pink", label="reference")
plt.ylabel('IMU-HEADING')
plt.xticks(rotation=45)
plt.axis([-1, 101, -100, 100])
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, gps, 'b.')
plt.plot(x, ref, color="pink", label="reference") 
plt.xlabel('time')
plt.ylabel('GPS-HEADING')

plt.xticks(rotation=45)
plt.axis([-1, 101, -100, 100])
plt.legend()

plt.show()
