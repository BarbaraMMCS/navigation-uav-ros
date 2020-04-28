cmake_minimum_required(VERSION 2.8.3)
project(ros_opencv_pkg)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

find_package(OpenCV REQUIRED)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(ros_opencv_pkg src/opencv_pub.cpp)

target_link_libraries(ros_opencv_pkg opencv_core opencv_highgui
   ${catkin_LIBRARIES}
)
