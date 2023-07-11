import csv
import rospy
from local_pkg.msg import Local

csv_file = '1.csv'

csv_header = ['gps_heading']
#csv_header = ['time','heading','gps_heading','speeed','gspeed','gear','headAcc']
#csv_header = ['x','y']

def callback(data):
    time = rospy.get_time()
    x = data.x
    y = data.y
    heading = data.heading
    gps_heading = data.gps_heading
    speeed = data.speeed
    gspeed = data.gspeed
    gear = data.gear
    headacc = data.headAcc

    with open(csv_file,'a') as file:
        writer = csv.writer(file)
        #writer.writerow([time,heading,gps_heading,speeed,gspeed,gear,headacc])
        writer.writerow([gps_heading])
        
def spring():
    rospy.init_node('data_logger', anonymous=True)

    with open(csv_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
    rospy.Subscriber('/local_msgs', Local, callback)

    rospy.spin()

if __name__ == '__main__':
    spring()