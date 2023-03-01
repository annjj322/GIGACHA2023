import threading
import rospy
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import Int32
from vision_msgs.msg import Detection2DArray

class Perception_():
   def __init__(self):
      rospy.Subscriber("/obstacles_markers", MarkerArray, self.lidar_callback)
      rospy.Subscriber("/traffic_bbox", Detection2DArray, self.traffic_callback)
      rospy.Subscriber("/Parking_num", Int32, self.parking_callback)

      self.signx = 0
      self.signy = 0
      self.objx = []
      self.objy = []
      self.objw = []
      self.objh = []
      self.tmp_objx = []
      self.tmp_objy = []
      self.tmp_objw = []
      self.tmp_objh = []
      self.tred = False
      self.tyellow = False
      self.tleft = False
      self.tgreen = False
      self.tmp_lidar_lock = threading.Lock()
      self.lidar_lock = threading.Lock()
      self.signname = ""
      self.parking_num = ""

   def lidar_callback(self, msg):
      if len(msg.markers) != 0:
         self.tmp_lidar_lock.acquire()
         tmp_objx = []
         tmp_objy = []
         tmp_objw = []
         tmp_objh = []
         for i in range(len(msg.markers)):
            tmp_objx.append(msg.markers[i].pose.position.x)
            tmp_objy.append(msg.markers[i].pose.position.y)
            tmp_objw.append(msg.markers[i].scale.y)
            tmp_objh.append(msg.markers[i].scale.x)
         self.tmp_objx = tmp_objx
         self.tmp_objy = tmp_objy
         self.tmp_objw = tmp_objw
         self.tmp_objh = tmp_objh
         self.tmp_lidar_lock.release()
      else:
         self.tmp_objx = []
         self.tmp_objy = []
         self.tmp_objw = []
         self.tmp_objh = []

   def traffic_callback(self, msg):
      if len(msg.detections) > 0:
         if msg.detections[0].results[0].id == 0:
            self.tred = True
            self.tyellow = False
            self.tleft = False
            self.tgreen = False
         elif msg.detections[0].results[0].id == 1:
            self.tred = False
            self.tyellow = True
            self.tleft = False
            self.tgreen = False
         elif msg.detections[0].results[0].id == 2:
            self.tred = False
            self.tyellow = False
            self.tleft = False
            self.tgreen = True
         elif msg.detections[0].results[0].id == 3:
            self.tred = True
            self.tyellow = False
            self.tleft = True
            self.tgreen = False
         elif msg.detections[0].results[0].id == 4:
            self.tred = False
            self.tyellow = False
            self.tleft = True
            self.tgreen = True

   def parking_callback(self, msg):
      ### HANAMJA JUCHA ###
      # self.parking_num = 2
      #####################
      self.parking_num = msg.data