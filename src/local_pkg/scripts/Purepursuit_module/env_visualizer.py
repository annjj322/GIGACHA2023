import rospy
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sig_int_handler import Activate_Signal_Interrupt_Handler

from sensor_msgs.msg import PointCloud, Imu
from geometry_msgs.msg import Point32
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry, Path
from visualization_msgs.msg import MarkerArray, Marker
from local_pkg.msg import Local
from local_pkg.msg import Path as customPath
from local_pkg.msg import Perception
from time import time

class environmentVisualizer:
    def __init__(self):
        
        # init node
        rospy.init_node("Environment_Visualizer", anonymous=False)
        
        # Subscriber
        rospy.Subscriber('/pose', Local, self.pose_callback)
        rospy.Subscriber('/global_path', customPath, self.globalpath_callback)
        rospy.Subscriber('/trajectory', customPath, self.localpath_callback)
        rospy.Subscriber('/perception', Perception, self.object_callback)
        # rospy.Subscriber('/simul_imu', Pose, self.simul_imu_callback) # simul
        rospy.Subscriber('/imu', Imu, self.simul_imu_callback) # real
        
        # Publisher
        self.vis_global_path_pub = rospy.Publisher("/vis_global_path", Path, queue_size=1) # using path
        self.vis_local_path_pub = rospy.Publisher("/vis_local_path", Path, queue_size=1) # using path
        
        self.vis_trajectory_pub = rospy.Publisher("/vis_trajectory", PointCloud, queue_size=1)
        self.vis_pose_pub = rospy.Publisher("/vis_position", Odometry, queue_size=1)
        
        self.vis_obj_pub = rospy.Publisher("/vis_obj", MarkerArray, queue_size=1)        

        # self.vis_global_path = PointCloud() # using pointcloud
        self.vis_global_path = Path() # using path
        self.vis_global_path.header.frame_id = "map"
        
        self.vis_local_path = Path() # using path
        self.vis_local_path.header.frame_id = "map"

        self.vis_local_path = Path() # using path
        self.vis_local_path.header.frame_id = "map"
        
        self.vis_trajectory = PointCloud()
        self.vis_trajectory.header.frame_id = "map"
        
        self.vis_pose = Odometry()
        self.vis_pose.header.frame_id = "map"

        # self.obsmap_pub = rospy.Publisher("/vis_map", PointCloud, queue_size=1)
        # self.obsmap = PointCloud()
        # self.obsmap.header.frame_id = "map"
    

        # self.local_path_pub = rospy.Publisher("/vis_local_path", PointCloud, queue_size=1)
        # self.obs_pub = rospy.Publisher("/vis_obs_pub", PointCloud, queue_size=1)
        # self.target_pub = rospy.Publisher("/vis_target", PointCloud, queue_size=1)

        # self.vis_local_path = PointCloud()
        # self.vis_local_path.header.frame_id = "map"


        # self.obs = PointCloud()
        # self.obs.header.frame_id = "map"

        # self.target = PointCloud()
        # self.target.header.frame_id = "map"

        self.t = time()
        
    def pose_callback(self, msg):
        ppoint = Point32()
        ppoint.x = msg.x
        ppoint.y = msg.y
        ppoint.z = 0
        self.vis_pose.pose.pose.position.x = ppoint.x
        self.vis_pose.pose.pose.position.y = ppoint.y
        self.vis_trajectory.header.stamp = rospy.Time.now()
        if self.t - time() < 0.5 :
            self.t = time()
            self.vis_trajectory.points.append(ppoint)

        # car heading
        # simul
        # heading = PoseStamped()
        # heading.pose.orientation = msg.heading
        # self.vis_pose.pose.pose.orientation.w = heading.pose.orientation

        # 
        # heading = Quaternion()
        # heading.w = msg.heading
        # self.vis_pose.pose.pose.orientation.w = heading.w

    def simul_imu_callback(self, msg):
        self.vis_pose.pose.pose.orientation = msg.orientation
        
    def globalpath_callback(self, msg):
        global_path = Path()
        for i in range(len(msg.x)):
            read_pose=PoseStamped()
            read_pose.pose.position.x = msg.x[i]
            read_pose.pose.position.y = msg.y[i]
            read_pose.pose.position.z = 0
            read_pose.pose.orientation.x=0
            read_pose.pose.orientation.y=0
            read_pose.pose.orientation.z=0
            read_pose.pose.orientation.w=1
            global_path.poses.append(read_pose)
        self.vis_global_path.poses = global_path.poses
        
        # global_path = PointCloud()
        # for i in range(len(msg.x)):
        #     gpoints = Point32()
        #     gpoints.x = msg.x[i]
        #     gpoints.y = msg.y[i]
        #     gpoints.z = 0
        #     global_path.points.append(gpoints)
        # self.vis_global_path.points = global_path.points
        
    def localpath_callback(self, msg):
        local_path = Path()
        for i in range(len(msg.x)):
            read_pose=PoseStamped()
            read_pose.pose.position.x = msg.x[i]
            read_pose.pose.position.y = msg.y[i]
            read_pose.pose.position.z = 0
            read_pose.pose.orientation.x=0
            read_pose.pose.orientation.y=0
            read_pose.pose.orientation.z=0
            read_pose.pose.orientation.w=1
            local_path.poses.append(read_pose)  
        self.vis_local_path.poses = local_path.poses
    
    def object_callback(self, msg):
        vis_obj = MarkerArray()
        c_id = 0
        
        for i in range(len(msg.objx)):
            circle_marker = Marker()
            circle_marker.header.frame_id = "map"
            circle_marker.header.stamp = rospy.Time.now()
            circle_marker.ns = "circles"
            circle_marker.id = c_id
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
            circle_marker.pose.position.x = msg.objx[i]
            circle_marker.pose.position.y = msg.objy[i]
            circle_marker.scale.x = 2.0 * msg.objr[i]
            circle_marker.scale.y = 2.0 * msg.objr[i]
            vis_obj.markers.append(circle_marker)
            c_id = c_id + 1
        
        self.vis_obj_pub.publish(vis_obj)
        

    def run(self):
        print(f"Publishing maps for visualization")
        # self.vis_global_path.header.stamp = rospy.Time.now()
        self.vis_global_path_pub.publish(self.vis_global_path)
        
        self.vis_local_path.header.stamp = rospy.Time.now()
        self.vis_local_path_pub.publish(self.vis_local_path)

        self.vis_trajectory_pub.publish(self.vis_trajectory)

        # self.vis_pose.header.stamp = rospy.Time.now()
        self.vis_pose_pub.publish(self.vis_pose)
        
        
        
        # self.obsmap.points = self.ego.obs_map.points
        # self.obsmap.header.stamp = rospy.Time.now()
        # self.obsmap_pub.publish(self.obsmap)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    vv = environmentVisualizer()
    rate = rospy.Rate(10)
    while True:
        vv.run()
        rate.sleep()
