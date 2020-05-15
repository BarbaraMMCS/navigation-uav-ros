# Project : Localization and detection of landmarks for supporting UAV navigation

Bachelor semester project 2 : part I

## Visualizing data with ROS

1. install ROS, understanding topic, publishers and subscribers

2. Rviz tool with http://www.cvlibs.net/datasets/kitti/raw_data.php

3. Implement nodes from prerecorded rosbag containing images, localization and other sensor data and display nodes in a more advanced way.

### Ros

<img src="media_files/ROS_diagram_1.png" width="1080">
          
### install workspace

### install this repository :
```
cd ~/catkin_ws/src

git clone https://github.com/BarbaraMMCS/UAV_navigation_ROS.git

cd ~/catkin_ws/

catkin_make

```
### Packages : 

vision_opencv : http://wiki.ros.org/vision_opencv

usb_cam : http://wiki.ros.org/usb_cam

### Launch :

```
roslaunch ros_visualise msg_node.launch
```
```
roslaunch ros_visualise image_node.launch
```
```
roslaunch ros_visualise video_ab.launch
```
```
roslaunch ros_visualise webcam.launch
```
```
roslaunch ros_visualise parameters.launch
```
```
roslaunch ros_visualise video_node.launch
```
<img src="media_files/new_save.png">

