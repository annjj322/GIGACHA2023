import threading
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
        self.perception = parent.shared.perception
        self.shared = parent.shared
        self.ego = parent.shared.ego

        self.global_path = self.shared.global_path  # from localizer
        self.parking = self.shared.park

        # Publisher
        self.vis_global_path_pub = rospy.Publisher(
            "/vis_global_path", Path, queue_size=1)  # using path
        self.vis_local_path_pub = rospy.Publisher(
            "/vis_local_path", Path, queue_size=1)  # using path
        self.vis_lattice_path_0_pub = rospy.Publisher(
            "/vis_lattice_path_0", Path, queue_size=1)
        self.vis_lattice_path_1_pub = rospy.Publisher(
            "/vis_lattice_path_1", Path, queue_size=1)
        self.vis_lattice_path_2_pub = rospy.Publisher(
            "/vis_lattice_path_2", Path, queue_size=1)
        self.vis_lattice_path_3_pub = rospy.Publisher(
            "/vis_lattice_path_3", Path, queue_size=1)

        self.vis_trajectory_pub = rospy.Publisher(
            "/vis_trajectory", PointCloud, queue_size=1)
        self.vis_pose_pub = rospy.Publisher(
            "/vis_position", Odometry, queue_size=1)

        self.vis_obj_pub1 = rospy.Publisher(
            "/vis_obj1", MarkerArray, queue_size=1)

        self.vis_parking_path_pub = rospy.Publisher(
            "/vis_parking_path", Path, queue_size=1)

        self.vis_trajectory_pub_dr = rospy.Publisher("/vis_trajectory_dr", PointCloud, queue_size=1)
        # self.vis_pose_pub_dr = rospy.Publisher("/vis_position_dr", Odometry, queue_size=1)

        self.vis_global_path = Path()  # using path
        self.vis_global_path.header.frame_id = "map"

        self.vis_local_path = Path()  # using path
        self.vis_local_path.header.frame_id = "map"

        self.vis_trajectory = PointCloud()
        self.vis_trajectory.header.frame_id = "map"

        self.vis_lattice_path_0 = Path()
        self.vis_lattice_path_0.header.frame_id = "map"

        self.vis_lattice_path_1 = Path()
        self.vis_lattice_path_1.header.frame_id = "map"

        self.vis_lattice_path_2 = Path()
        self.vis_lattice_path_2.header.frame_id = "map"

        self.vis_lattice_path_3 = Path()
        self.vis_lattice_path_3.header.frame_id = "map"

        self.vis_parking_path = Path()
        self.vis_parking_path.header.frame_id = "map"

        self.vis_trajectory_dr = PointCloud()
        self.vis_trajectory_dr.header.frame_id = "map"

        self.vis_pose = Odometry()
        self.vis_pose.header.frame_id = "map"

        self.vis_pose_dr = Odometry()
        self.vis_pose_dr.header.frame_id = "map"

        self.t = time()
        self.d = time()

    def run(self):
        while True:
            try:
                self.cut_path = self.shared.cut_path
                self.lattice_path = self.shared.lattice_path  # from LPP []
                self.local_path = self.lattice_path[self.shared.selected_lane]
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
                self.vis_trajectory_dr.header.stamp = rospy.Time.now()
                self.vis_pose_dr.pose.pose.orientation = self.ego.orientation
                if self.d - time() < 0.5 :
                    self.d = time()
                    self.vis_trajectory_dr.points.append(ppoint_dr)

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

                #################################### LOCAL PATH ################################################

                local_path = Path()
                for i in range(len(self.local_path.x)):
                    read_pose = PoseStamped()
                    read_pose.pose.position.x = self.local_path.x[i]
                    read_pose.pose.position.y = self.local_path.y[i]
                    read_pose.pose.position.z = 0
                    read_pose.pose.orientation.x = 0
                    read_pose.pose.orientation.y = 0
                    read_pose.pose.orientation.z = 0
                    read_pose.pose.orientation.w = 1
                    local_path.poses.append(read_pose)
                self.vis_local_path.poses = local_path.poses

                #################################### LATTICE PATHS ################################################

                lattice_path_0 = Path()
                lattice_path_1 = Path()
                lattice_path_2 = Path()
                lattice_path_3 = Path()

                for i in range(len(self.lattice_path)):
                    for j in range(len(self.lattice_path[0].x)):
                        read_pose = PoseStamped()
                        read_pose.pose.position.x = self.lattice_path[i].x[j]
                        read_pose.pose.position.y = self.lattice_path[i].y[j]
                        read_pose.pose.position.z = 0
                        read_pose.pose.orientation.x = 0
                        read_pose.pose.orientation.y = 0
                        read_pose.pose.orientation.z = 0
                        read_pose.pose.orientation.w = 1
                        if i == 0:
                            lattice_path_0.poses.append(read_pose)
                        elif i == 1:
                            lattice_path_1.poses.append(read_pose)
                        elif i == 2:
                            lattice_path_2.poses.append(read_pose)
                        elif i == 3:
                            lattice_path_3.poses.append(read_pose)
                self.vis_lattice_path_0.poses = lattice_path_0.poses
                self.vis_lattice_path_1.poses = lattice_path_1.poses
                self.vis_lattice_path_2.poses = lattice_path_2.poses
                self.vis_lattice_path_3.poses = lattice_path_3.poses


                #############################object#########################################

                vis_obj1 = MarkerArray()
                c_id1 = 0

                for i in range(len(self.perception.objx)):
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
                    circle_marker.color.r = 0.2
                    circle_marker.color.g = 0.8
                    circle_marker.color.b = 0.2
                    circle_marker.color.a = 1.0
                    circle_marker.lifetime = rospy.Duration(0.1)
                    circle_marker.pose.position.x = self.perception.objx[i]
                    circle_marker.pose.position.y = self.perception.objy[i]
                    circle_marker.scale.x = (self.perception.objw[i]+1)
                    circle_marker.scale.y = (self.perception.objw[i]+1)
                    vis_obj1.markers.append(circle_marker)
                    c_id1 = c_id1 + 1

                ######################## PARKING PATH ##########################
                parking = Path()
                for i in range(len(self.parking.forward_path.x)):
                    read_pose = PoseStamped()
                    read_pose.pose.position.x = self.parking.forward_path.x[i]
                    read_pose.pose.position.y = self.parking.forward_path.y[i]
                    read_pose.pose.position.z = 0
                    read_pose.pose.orientation.x = 0
                    read_pose.pose.orientation.y = 0
                    read_pose.pose.orientation.z = 0
                    read_pose.pose.orientation.w = 1
                    parking.poses.append(read_pose)
                self.vis_parking_path.poses = parking.poses

                # publish
                self.vis_obj_pub1.publish(vis_obj1)

                self.vis_global_path.header.stamp = rospy.Time.now()
                self.vis_global_path_pub.publish(self.vis_global_path)

                self.vis_local_path.header.stamp = rospy.Time.now()
                self.vis_local_path_pub.publish(self.vis_local_path)

                self.vis_lattice_path_0.header.stamp = rospy.Time.now()
                self.vis_lattice_path_0_pub.publish(self.vis_lattice_path_0)

                self.vis_lattice_path_1.header.stamp = rospy.Time.now()
                self.vis_lattice_path_1_pub.publish(self.vis_lattice_path_1)

                self.vis_lattice_path_2.header.stamp = rospy.Time.now()
                self.vis_lattice_path_2_pub.publish(self.vis_lattice_path_2)

                self.vis_lattice_path_3.header.stamp = rospy.Time.now()
                self.vis_lattice_path_3_pub.publish(self.vis_lattice_path_3)

                self.vis_parking_path.header.stamp = rospy.Time.now()
                self.vis_parking_path_pub.publish(self.vis_parking_path)

                self.vis_trajectory_pub.publish(self.vis_trajectory)

                self.vis_trajectory_pub_dr.publish(self.vis_trajectory_dr)

                self.vis_pose_pub.publish(self.vis_pose)
                # self.vis_pose_pub_dr.publish(self.vis_pose_dr)
            except IndexError:
                print("++++++++env_visualizer+++++++++")
            sleep(self.period)
