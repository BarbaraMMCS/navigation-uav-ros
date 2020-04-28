cmake_minimum_required(VERSION 2.8.3)
project(ros_opencv_pkg)

find_package(catkin REQUIRED COMPONENTS
    roscpp
    rospy
    opencv
    std_msgs
    cv_bridge
    image_transport
    sensor_msgs
)

find_package(OpenCV)

include_directories(${OpenCV_INCLUDE_DIRS})

target_link_libraries(my_awesome_library ${OpenCV_LIBRARIES})


catkin_package(CATKIN_DEPENDS
    roscpp
    rospy
    opencv
    std_msgs
    cv_bridge
    image_transport
    sensor_msgs
)

include_directories(${catkin_INCLUDE_DIRS})
