# Project : Localization and detection of landmarks for supporting UAV navigation

Bachelor semester project 2 : part I

## Visualizing data with ROS

1. install ROS, understanding topic, publishers and subscribers

2. Rviz tool with http://www.cvlibs.net/datasets/kitti/raw_data.php

3. Implement nodes from prerecorded rosbag containing images, localization and other sensor data and display nodes in a more advanced way.

### Ros

<img src="media/ROS_diagram_1.png" width="1080">
          
### install workspace :

```
mkdir -p ~/catkin_ws/src

cd ~/catkin_ws/

catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3

source devel/setup.bash
```

### install this repository :
```
cd ~/catkin_ws/src

git clone https://github.com/BarbaraMMCS/UAV_navigation_ROS.git

cd ~/catkin_ws/

catkin_make

```
### install Package : 

vision_opencv : http://wiki.ros.org/vision_opencv

cv_camera : http://wiki.ros.org/cv_camera

usb_cam : http://wiki.ros.org/usb_cam

### launch nodes :

Message node
```
roslaunch visualise_ros node.launch
```
Image node
```
roslaunch visualise_ros image.launch
```
Video node A - B 
```
roslaunch visualise_ros video.launch
```
Camera topic node
```
roslaunch visualise_ros webcam.launch
```
Fps parameter launch
```
roslaunch visualise_ros fps_param.launch
```
Video node with filters and sliders
```
roslaunch visualise_ros camera_node.launch
```
<img src="media/new_save.png">

