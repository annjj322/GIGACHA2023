import threading
import rospy
from geometry_msgs.msg import PoseArray
class Perception_():
   def __init__(self):
      rospy.Subscriber("/pcd", PoseArray, self.obs_callback)

      self.rx = None
      self.ry = None

      self.parrallel_flag = True
      self.delivery_flag = True     
      self.diagonal_flag = True      
   
   def obs_callback(self, msg):
      if len(msg.markers) != 0:
         self.rx = msg.x
         self.ry = msg.y
         print("obs info from LiDAR callbacked")

         # l = ((self.L + self.rx)**2 + (self.ry)**2)**0.5
         # cx = self.shared.ego.x + l*cos(radians(self.shared.ego.heading) - atan(self.ry/(self.rx + self.L))) # 이게 중요
         # cy = self.shared.ego.y + l*sin(radians(self.shared.ego.heading) - atan(self.ry/(self.rx + self.L))) # 이게 중요
