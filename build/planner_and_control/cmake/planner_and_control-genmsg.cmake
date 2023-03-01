# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "planner_and_control: 12 messages, 0 services")

set(MSG_I_FLAGS "-Iplanner_and_control:/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Iplanner_and_control:/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(planner_and_control_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg" "geometry_msgs/Point"
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg" "geometry_msgs/Point"
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg" "planner_and_control/SegmentObstacle:geometry_msgs/Point:planner_and_control/CircleObstacle:std_msgs/Header"
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg" ""
)

get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg" NAME_WE)
add_custom_target(_planner_and_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "planner_and_control" "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg"
  "${MSG_I_FLAGS}"
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)
_generate_msg_cpp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
)

### Generating Services

### Generating Module File
_generate_module_cpp(planner_and_control
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(planner_and_control_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(planner_and_control_generate_messages planner_and_control_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_cpp _planner_and_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(planner_and_control_gencpp)
add_dependencies(planner_and_control_gencpp planner_and_control_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS planner_and_control_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg"
  "${MSG_I_FLAGS}"
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)
_generate_msg_eus(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
)

### Generating Services

### Generating Module File
_generate_module_eus(planner_and_control
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(planner_and_control_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(planner_and_control_generate_messages planner_and_control_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_eus _planner_and_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(planner_and_control_geneus)
add_dependencies(planner_and_control_geneus planner_and_control_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS planner_and_control_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg"
  "${MSG_I_FLAGS}"
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)
_generate_msg_lisp(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
)

### Generating Services

### Generating Module File
_generate_module_lisp(planner_and_control
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(planner_and_control_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(planner_and_control_generate_messages planner_and_control_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_lisp _planner_and_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(planner_and_control_genlisp)
add_dependencies(planner_and_control_genlisp planner_and_control_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS planner_and_control_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg"
  "${MSG_I_FLAGS}"
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)
_generate_msg_nodejs(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
)

### Generating Services

### Generating Module File
_generate_module_nodejs(planner_and_control
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(planner_and_control_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(planner_and_control_generate_messages planner_and_control_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_nodejs _planner_and_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(planner_and_control_gennodejs)
add_dependencies(planner_and_control_gennodejs planner_and_control_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS planner_and_control_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg"
  "${MSG_I_FLAGS}"
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg;/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)
_generate_msg_py(planner_and_control
  "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
)

### Generating Services

### Generating Module File
_generate_module_py(planner_and_control
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(planner_and_control_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(planner_and_control_generate_messages planner_and_control_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg" NAME_WE)
add_dependencies(planner_and_control_generate_messages_py _planner_and_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(planner_and_control_genpy)
add_dependencies(planner_and_control_genpy planner_and_control_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS planner_and_control_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/planner_and_control
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(planner_and_control_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(planner_and_control_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET planner_and_control_generate_messages_cpp)
  add_dependencies(planner_and_control_generate_messages_cpp planner_and_control_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/planner_and_control
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(planner_and_control_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(planner_and_control_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET planner_and_control_generate_messages_eus)
  add_dependencies(planner_and_control_generate_messages_eus planner_and_control_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/planner_and_control
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(planner_and_control_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(planner_and_control_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET planner_and_control_generate_messages_lisp)
  add_dependencies(planner_and_control_generate_messages_lisp planner_and_control_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/planner_and_control
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(planner_and_control_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(planner_and_control_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET planner_and_control_generate_messages_nodejs)
  add_dependencies(planner_and_control_generate_messages_nodejs planner_and_control_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/planner_and_control
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(planner_and_control_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(planner_and_control_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET planner_and_control_generate_messages_py)
  add_dependencies(planner_and_control_generate_messages_py planner_and_control_generate_messages_py)
endif()
