cmake_minimum_required(VERSION 2.8.3)
project(video)


find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  rospy
  std_msgs
)



catkin_package( 
  LIBRARIES video
  CATKIN_DEPENDS  
  cv_bridge
  rospy
  message_runtime
  std_msgs
)


include_directories(${catkin_INCLUDE_DIRS})
