# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "track_pkg: 1 messages, 0 services")

set(MSG_I_FLAGS "-Itrack_pkg:/home/gigacha/TEAM-GIGACHA/src/track_pkg/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg")

# Find all generators

add_custom_target(track_pkg_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/track_pkg/msg/gigacha.msg" NAME_WE)
add_custom_target(_track_pkg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "track_pkg" "/home/gigacha/TEAM-GIGACHA/src/track_pkg/msg/gigacha.msg" ""
)

#
#  langs = 
#


