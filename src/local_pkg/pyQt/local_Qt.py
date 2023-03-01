import sys
import rospy
from local_pkg.msg import Local
from local_pkg.msg import Serial_Info
from local_pkg.msg import Control_Info
from local_pkg.msg import Guii
from geometry_msgs.msg import Pose
from sensor_msgs.msg import NavSatFix 
from ublox_msgs.msg import NavPVT 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("uis/local_ui.ui")[0]

global checker_list
checker_list = [False, False, False]


class WindowClass(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        rospy.init_node("Gigacha_ui", anonymous = False)
        rospy.Subscriber("/local_msgs", Local, self.localCallback)
        rospy.Subscriber("/from_master", Guii, self.masterCallback)
        rospy.Subscriber("ublox_gps/fix", NavSatFix, self.gpsCallback) 
        rospy.Subscriber("ublox_gps/navpvt", NavPVT, self.navpvtCallback) 
        rospy.Subscriber("/serial", Serial_Info, self.serialCallback)
        rospy.Subscriber("/simul_gps", Pose, self.simulGpsCallback)
        rospy.Subscriber("/controller", Control_Info, self.controlCallback)

        self.dial_heading.setMaximum(180)
        self.dial_heading.setMinimum(-180)

        self.dial_steer.setMaximum(30)
        self.dial_steer.setMinimum(-30)

        self.slider_speed.setMaximum(20)
        self.slider_speed.setMinimum(0)
        self.slider_brake.setMaximum(200)
        self.slider_brake.setMinimum(0)

        self.rbtn_localizer.setAutoExclusive(False)
        self.rbtn_mission_pln.setAutoExclusive(False)
        self.rbtn_behavior_pln.setAutoExclusive(False)
        self.rbtn_motion_pln.setAutoExclusive(False)
        self.rbtn_lat_con.setAutoExclusive(False)
        self.rbtn_lon_con.setAutoExclusive(False)

    def masterCallback(self, msg):
        self.lbl_index.setText(str(msg.index))
        self.lbl_mission.setText(msg.mission)
        self.lbl_behavior.setText(msg.behavior)

        self.rbtn_localizer.setChecked(msg.local)
        self.rbtn_mission_pln.setChecked(msg.mission_pln)
        self.rbtn_behavior_pln.setChecked(msg.behavior_pln)
        self.rbtn_motion_pln.setChecked(msg.motion_pln)
        self.rbtn_lat_con.setChecked(msg.con)

    def localCallback(self, msg):
        self.lbl_x.setText(str(msg.x))
        self.lbl_y.setText(str(msg.y))
        self.lbl_drx.setText(str(msg.dr_x))
        self.lbl_dry.setText(str(msg.dr_y))

        if 0 <= msg.heading < 180:
            heading = msg.headin
        else:
            heading = msg.heading - 360

        self.dial_heading.setValue(int(heading))
        self.lbl_heading.setText(str(msg.heading))

    def controlCallback(self, msg):
        self.dial_steer.setValue(int(msg.steer))
        self.lbl_steer.setText("{0}".format(self.dial_steer.value()))

        if msg.gear == 0:
            self.lbl_gear.setText("Forward")
        elif msg.gear == 2:
            self.lbl_gear.setText("Backward")

    def serialCallback(self, data):
        self.slider_speed.setValue(round(data.speed))
        self.lbl_speed.setText("{0} km/h".format(self.slider_speed.value()))

        self.slider_brake.setValue(data.brake)
        self.lbl_brake.setText("{0}".format(self.slider_brake.value()))

        if data.auto_manual == 1:
            self.lbl_ma.setText("AUTO")
        else:
            self.lbl_ma.setText("MANUAL")

    def gpsCallback(self, data):
        self.lbl_lat.setText(str(data.latitude))
        self.lbl_lon.setText(str(data.longitude))

    def navpvtCallback(self, data):
        self.lbl_acc.setText("{0}".format(data.hAcc))

        if data.hAcc < 50:
            self.lbl_rtk.setText("ON")
        else:
            self.lbl_rtk.setText("OFF")

        if data.fixType == 0:
            self.lbl_gnss.setText("UNAVAILABLE")
        elif data.fixType == 1:
            self.lbl_gnss.setText("INACCURACY")
        elif data.fixType == 2:
            self.lbl_gnss.setText("GNSS - 3sat")
        elif data.fixType == 3:
            self.lbl_gnss.setText("GNSS - 12sat")
        elif data.fixType == 4:
            self.lbl_gnss.setText("DIFF")
        else:
            self.lbl_gnss.setText("FIX")

    def simulGpsCallback(self, data):
        self.lbl_lat.setText(str(data.position.x))
        self.lbl_lon.setText(str(data.position.y))

    def initUI(self):
        self.setWindowTitle('Local Informations')
        self.setWindowIcon(QIcon("location.png"))
        self.setGeometry(300, 300, 700, 550)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())