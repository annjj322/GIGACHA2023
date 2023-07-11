import threading
import rospy
from time import sleep, time
#이게 쓰레드버전
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
        self.perception = parent.shared.perception
        self.shared = parent.shared
        self.ego = parent.shared.ego

        self.global_path = self.shared.global_path  # from localizer
        self.parking = self.shared.park

        # Publisher
        self.vis_global_path_pub = rospy.Publisher(
            "/vis_global_path", Path, queue_size=1)  # using path
                

        self.vis_trajectory_pub = rospy.Publisher(
            "/vis_trajectory", PointCloud, queue_size=1)
        self.vis_pose_pub = rospy.Publisher(
            "/vis_position", Odometry, queue_size=1)

        self.vis_trajectory_pub_dr = rospy.Publisher("/vis_trajectory_dr", PointCloud, queue_size=1)

        self.vis_global_path = Path()  # using path
        self.vis_global_path.header.frame_id = "map"

        self.vis_trajectory = PointCloud()
        self.vis_trajectory.header.frame_id = "map"

        self.vis_pose = Odometry()
        self.vis_pose.header.frame_id = "map"

        self.vis_pose_dr = Odometry()
        self.vis_pose_dr.header.frame_id = "map"

        self.t = time()
        self.d = time()

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
                self.vis_pose.twist.twist.linear.x = self.ego.heading
                self.vis_trajectory.header.stamp = rospy.Time.now()
                if self.t - time() < 0.5:
                    self.t = time()
                    self.vis_trajectory.points.append(ppoint)

                # dead reckoning
                ppoint_dr = Point32()
                ppoint_dr.x = self.ego.dr_x
                ppoint_dr.y = self.ego.dr_y
                ppoint_dr.z = 0
                self.vis_pose_dr.pose.pose.position.x = ppoint_dr.x
                self.vis_pose_dr.pose.pose.position.y = ppoint_dr.y
                self.vis_pose_dr.pose.pose.orientation = self.ego.orientation

                ############################# GLOBAL PATH ########################################
                gp = Path()
                for i in range(len(self.global_path.x)):
                    read_pose = PoseStamped()
                    read_pose.pose.position.x = self.global_path.x[i]
                    read_pose.pose.position.y = self.global_path.y[i]
                    read_pose.pose.position.z = 0
                    read_pose.pose.orientation.x = 0
                    read_pose.pose.orientation.y = 0
                    read_pose.pose.orientation.z = 0
                    read_pose.pose.orientation.w = 1
                    gp.poses.append(read_pose)
                self.vis_global_path.poses = gp.poses

                
        
                # publish

                self.vis_global_path.header.stamp = rospy.Time.now()
                self.vis_global_path_pub.publish(self.vis_global_path)

                self.vis_trajectory_pub.publish(self.vis_trajectory)

                self.vis_pose_pub.publish(self.vis_pose)

            except IndexError:
                print("++++++++env_visualizer+++++++++")
            sleep(self.period)
