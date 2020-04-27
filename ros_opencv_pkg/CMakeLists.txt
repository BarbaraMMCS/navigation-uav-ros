cmake_minimum_required(VERSION 2.8.3)
project(ros_opencv_pkg)

find_package(catkin REQUIRED COMPONENTS
    roscpp
    rospy
    std_msgs
    #cv_bridge
    #image_transport
    #sensor_msgs
)


catkin_package(CATKIN_DEPENDS
    roscpp
    rospy
    std_msgs
    #cv_bridge
    #image_transport
    #sensor_msgs
)

include_directories(${catkin_INCLUDE_DIRS})
