# Project : Localization and detection of landmarks for supporting UAV navigation

Bachelor semester project 2 : part I

## Visualizing data with ROS

1. install ROS, understanding topic, publishers and subscribers

2. Rviz tool with http://www.cvlibs.net/datasets/kitti/raw_data.php

3. Implement nodes from prerecorded rosbag containing images, localization and other sensor data and display nodes in a more advanced way.

## Ros

<img src="files/file.png" width="1080">
          
### Install workspace

### Install this repository :
```
cd ~/catkin_ws/src

git clone https://github.com/BarbaraMMCS/UAV_navigation_ROS.git

cd ~/catkin_ws/

catkin_make

```
### Packages: 

vision_opencv : http://wiki.ros.org/vision_opencv

usb_cam : http://wiki.ros.org/usb_cam

### Launch:
```
roslaunch ros_visualise main.launch
```
```
roslaunch ros_edge_detector main.launch
```
```
roslaunch ros_fps time.launch
```
### ros_visualise:

<img src="files/from_file.png">

```
rosrun rviz rviz -d `rospack find ros_visualise`/rviz/image.rviz
```
<img src="files/rqt.png">

### ros_edge_detector:
<img src="files/edge.png">
<img src="files/detected.png">
<img src="files/both.png">
<img src="files/all.png">
<img src="files/connected.png">

## Kitty data set: 
```
http://www.cvlibs.net/datasets/kitti/index.php
```
<img src="files/kitti_rviz.png">

```
rosrun rviz rviz -d `rospack find ros_visualise`/rviz/kitti.rviz
```

<img src="files/kitti_node.png">


<img src="files/on_rosbag.png">





<img src="files/image.png">

