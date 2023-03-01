import threading
import struct
import rospy
from time import sleep, time

from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry, Path
from visualization_msgs.msg import MarkerArray, Marker

class Visualizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.ego = parent.shared.ego
        self.shared = parent.shared
        self.ego = parent.shared.ego
        self.perception = parent.shared.perception

        self.global_path = self.shared.global_path # from localizer
        
        # Publisher
        self.vis_global_path_pub = rospy.Publisher("/vis_global_path", Path, queue_size=1) # using path
        
        self.vis_trajectory_pub = rospy.Publisher("/vis_trajectory", PointCloud, queue_size=1)
        self.vis_pose_pub = rospy.Publisher("/vis_position", Odometry, queue_size=1)
        
        self.vis_target_pub = rospy.Publisher("/vis_obj", Marker, queue_size=1)
        self.vis_yellow_pub = rospy.Publisher("/vis_yellow", MarkerArray, queue_size=1)
        self.vis_blue_pub = rospy.Publisher("/vis_blue", MarkerArray, queue_size=1)

        self.vis_global_path = Path() # using path
        self.vis_global_path.header.frame_id = "map"
        
        self.vis_trajectory = PointCloud()
        self.vis_trajectory.header.frame_id = "map"
        
        self.vis_pose = Odometry()
        self.vis_pose.header.frame_id = "map"

        self.t = time()

    def run(self):
        while True:
            try:
                ######################### POSE ##############################
                
                ppoint = Point32()
                ppoint.x = self.ego.x
                ppoint.y = self.ego.y
                ppoint.z = 0
                self.vis_pose.pose.pose.position.x = self.ego.x
                self.vis_pose.pose.pose.position.y = self.ego.y
                self.vis_pose.pose.pose.orientation = self.ego.orientation
                # print(self.vis_pose.pose.pose.orientation)
                self.vis_trajectory.header.stamp = rospy.Time.now()
                if self.t - time() < 0.5 :
                    self.t = time()
                    self.vis_trajectory.points.append(ppoint)

                ############################# GLOBAL PATH ########################################
                gp = Path()
                for i in range(len(self.global_path.x)):
                    read_pose=PoseStamped()
                    read_pose.pose.position.x = self.global_path.x[i]
                    read_pose.pose.position.y = self.global_path.y[i]
                    read_pose.pose.position.z = 0
                    read_pose.pose.orientation.x=0
                    read_pose.pose.orientation.y=0
                    read_pose.pose.orientation.z=0
                    read_pose.pose.orientation.w=1
                    gp.poses.append(read_pose)
                self.vis_global_path.poses = gp.poses


                ##################### target point #############################
                vis_target_marker = Marker()
                vis_target_marker.header.frame_id = "map"
                vis_target_marker.header.stamp = rospy.Time()
                vis_target_marker.ns = "circles"
                vis_target_marker.id = 0
                vis_target_marker.type = Marker.CYLINDER
                vis_target_marker.action = Marker.ADD
                vis_target_marker.pose.position.x = self.ego.point_x
                vis_target_marker.pose.position.y = self.ego.point_y
                vis_target_marker.pose.position.z = 0
                vis_target_marker.pose.orientation.x = 0.0
                vis_target_marker.pose.orientation.y = 0.0
                vis_target_marker.pose.orientation.z = 0.0
                vis_target_marker.pose.orientation.w = 1.0
                vis_target_marker.scale.x = 0.5
                vis_target_marker.scale.y = 0.5
                vis_target_marker.scale.z = 0.1
                vis_target_marker.color.r = 255
                vis_target_marker.color.g = 0
                vis_target_marker.color.b = 0
                vis_target_marker.color.a = 1
                vis_target_marker.lifetime = rospy.Duration(0.1)

                ################## yellow cone ##################################

                vis_yellow = MarkerArray()
                c_id1 = 0

                for i in range(len(self.perception.left_obs)):
                    circle_marker = Marker()
                    circle_marker.header.frame_id = "map"
                    circle_marker.header.stamp = rospy.Time.now()
                    circle_marker.ns = "circles"
                    circle_marker.id = c_id1
                    circle_marker.type = Marker.CYLINDER
                    circle_marker.action = Marker.ADD
                    circle_marker.pose.position.z = -0.1
                    circle_marker.pose.orientation.x = 0.0
                    circle_marker.pose.orientation.y = 0.0
                    circle_marker.pose.orientation.z = 0.0
                    circle_marker.pose.orientation.w = 1.0
                    circle_marker.scale.z = 0.1
                    circle_marker.color.r = 255
                    circle_marker.color.g = 255
                    circle_marker.color.b = 0
                    circle_marker.color.a = 1
                    circle_marker.lifetime = rospy.Duration(0.1)
                    circle_marker.pose.position.x = self.perception.left_obs[i][0]
                    circle_marker.pose.position.y = self.perception.left_obs[i][1]
                    circle_marker.scale.x = 0.75
                    circle_marker.scale.y = 0.75
                    vis_yellow.markers.append(circle_marker)
                    c_id1 = c_id1 + 1
                    


                ############### blue cone ###################################

                vis_blue = MarkerArray()
                c_id2 = 0

                for i in range(len(self.perception.right_obs)):
                    circle_marker = Marker()
                    circle_marker.header.frame_id = "map"
                    circle_marker.header.stamp = rospy.Time.now()
                    circle_marker.ns = "circles"
                    circle_marker.id = c_id2
                    circle_marker.type = Marker.CYLINDER
                    circle_marker.action = Marker.ADD
                    circle_marker.pose.position.z = -0.1
                    circle_marker.pose.orientation.x = 0.0
                    circle_marker.pose.orientation.y = 0.0
                    circle_marker.pose.orientation.z = 0.0
                    circle_marker.pose.orientation.w = 1.0
                    circle_marker.scale.z = 0.1
                    circle_marker.color.r = 0
                    circle_marker.color.g = 255
                    circle_marker.color.b = 0
                    circle_marker.color.a = 1
                    circle_marker.lifetime = rospy.Duration(0.1)
                    circle_marker.pose.position.x = self.perception.right_obs[i][0]
                    circle_marker.pose.position.y = self.perception.right_obs[i][1]
                    circle_marker.scale.x = 0.75
                    circle_marker.scale.y = 0.75
                    vis_blue.markers.append(circle_marker)
                    c_id2 = c_id2 + 1
                # publish
                
                self.vis_target_pub.publish(vis_target_marker)
                self.vis_yellow_pub.publish(vis_yellow)
                self.vis_blue_pub.publish(vis_blue)

                self.vis_global_path.header.stamp = rospy.Time.now()
                self.vis_global_path_pub.publish(self.vis_global_path)
                
                self.vis_trajectory_pub.publish(self.vis_trajectory)

                self.vis_pose_pub.publish(self.vis_pose)

            except IndexError:
                print("+++++++++++++++++")
                
            sleep(self.period)