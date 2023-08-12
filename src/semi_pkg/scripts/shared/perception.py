import threading
import rospy
from geometry_msgs.msg import PoseArray
from visualization_msgs.msg import MarkerArray

class Perception_():
   def __init__(self):
      rospy.Subscriber("/pcd", PoseArray, self.obs_callback)
      rospy.Subscriber("/left_markers/Global",MarkerArray,self.narrow_callback)
      rospy.Subscriber("/right_markers/Global",MarkerArray,self.narrow_callback)
      # rospy.Subscriber("/mapOptmization/inner_markers",MarkerArray,self.narrow_callback)
      # rospy.Subscriber("/mapOptmization/outer_markers",MarkerArray,self.narrow_callback)
      rospy.Subscriber("/left_markers/Local",MarkerArray,self.narrow_local_callback)
      rospy.Subscriber("/right_markers/Local",MarkerArray,self.narrow_local_callback)
      rospy.Subscriber("/stop_local",MarkerArray,self.local2Global)
      rospy.Subscriber("/markers",MarkerArray,self.obs_callback)

      self.rx = None
      self.ry = None

      self.parrallel_flag = True
      self.delivery_flag = True     
      self.diagonal_flag = True      
   
      self.inner_x = []
      self.inner_y = []
      self.outer_x = []
      self.outer_y = []

      self.left_x = []
      self.left_y = []
      self.right_x = []
      self.right_y = []

      
      self.local2global = False

      ##obs_avoidance_labotary
      self.obs_list = []

      
   def obs_callback(self, msg):
      if len(msg.markers) != 0:
         self.rx = msg.x
         self.ry = msg.y
         print("obs info from LiDAR callbacked")

         # l = ((self.L + self.rx)**2 + (self.ry)**2)**0.5
         # cx = self.shared.ego.x + l*cos(radians(self.shared.ego.heading) - atan(self.ry/(self.rx + self.L))) # 이게 중요
         # cy = self.shared.ego.y + l*sin(radians(self.shared.ego.heading) - atan(self.ry/(self.rx + self.L))) # 이게 중요

   def narrow_local_callback(self, msg):
      try:
         if len(self.left_x) != 0 and len(self.right_x) != 0:
            self.left_x = []
            self.left_y = []
            self.right_x = []
            self.right_y = []
         for marker in msg.markers: # start id = 10 and 30
            if marker.id < 30:
               self.left_x.append(marker.pose.position.x)
               self.left_y.append(marker.pose.position.y)
            else:
               self.right_x.append(marker.pose.position.x)
               self.right_y.append(marker.pose.position.y)
      except IndexError:
         print("narrow_local_callback_error")

   def narrow_callback(self, msg):
      try:
         if len(self.inner_x ) == 0:
            for marker in msg.markers:
               if 100 < marker.id < 300:
                  self.inner_x.append(marker.pose.position.x)
                  self.inner_y.append(marker.pose.position.y)
            self.inner_x.append(self.inner_x[0])
            self.inner_y.append(self.inner_y[0])      
         elif len(self.outer_x) == 0:
            for marker in msg.markers:
               if marker.id >= 300:
                  self.outer_x.append(marker.pose.position.x)
                  self.outer_y.append(marker.pose.position.y)
            self.outer_x.append(self.outer_x[0])
            self.outer_y.append(self.outer_y[0])   
      except IndexError:
         print('narrow_callback_error')

   def local2Global(self, msg):
      self.local2global = True

   def obs_callback(self, data):
      self.obs_list = []
      for marker in data.markers:
         x = marker.pose.position.x
         y = marker.pose.position.y
         width = marker.pose.scale.y
         length = marker.pose.scale.x
         self.obs_list.append([[x,y],width,length])