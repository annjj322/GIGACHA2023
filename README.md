TEAM GIGACHA

inhagigacha repo url
https://github.com/inhagigacha/Phase1_Team2

![system flow](system_flow/gigacha_system.io.drawio.png)

Local
Planning
LiDAR
Vision


# TEAM-GIGACHA
2022 GIGACHA 
실행 방법

3d 객체 검출
roslaunch velodyne_pointcloud VLP16_points.launch
roslaunch lidar3d_od lidar_main.launch

협로주행
roslaunch velodyne_pointcloud VLP16_points.launch
roslaunch narrow_road_drive narrow_drive.launch
rosrun narrow_road_drive narrow_road.py
