cmake_minimum_required(VERSION 2.8.3)
project(image)

find_package(catkin REQUIRED COMPONENTS
  roslaunch
  cv_bridge
  rospy
  sensor_msgs
  std_msgs
)

find_package(OpenCV REQUIRED)

include_directories(${catkin_INCLUDE_DIRS})
