# Install script for directory: /home/gigacha/TEAM-GIGACHA/src/planner_and_control

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/gigacha/TEAM-GIGACHA/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/planner_and_control/msg" TYPE FILE FILES
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Local.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Gngga.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Path.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Serial_Info.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Control_Info.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Ego.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Obstacles.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/CircleObstacle.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/SegmentObstacle.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Sign.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Perception.msg"
    "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/msg/Parking.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/planner_and_control/cmake" TYPE FILE FILES "/home/gigacha/TEAM-GIGACHA/build/planner_and_control/catkin_generated/installspace/planner_and_control-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/gigacha/TEAM-GIGACHA/devel/include/planner_and_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/gigacha/TEAM-GIGACHA/devel/share/roseus/ros/planner_and_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/gigacha/TEAM-GIGACHA/devel/share/common-lisp/ros/planner_and_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/gigacha/TEAM-GIGACHA/devel/share/gennodejs/ros/planner_and_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/gigacha/TEAM-GIGACHA/devel/lib/python2.7/dist-packages/planner_and_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/gigacha/TEAM-GIGACHA/devel/lib/python2.7/dist-packages/planner_and_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/gigacha/TEAM-GIGACHA/build/planner_and_control/catkin_generated/installspace/planner_and_control.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/planner_and_control/cmake" TYPE FILE FILES "/home/gigacha/TEAM-GIGACHA/build/planner_and_control/catkin_generated/installspace/planner_and_control-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/planner_and_control/cmake" TYPE FILE FILES
    "/home/gigacha/TEAM-GIGACHA/build/planner_and_control/catkin_generated/installspace/planner_and_controlConfig.cmake"
    "/home/gigacha/TEAM-GIGACHA/build/planner_and_control/catkin_generated/installspace/planner_and_controlConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/planner_and_control" TYPE FILE FILES "/home/gigacha/TEAM-GIGACHA/src/planner_and_control/package.xml")
endif()

