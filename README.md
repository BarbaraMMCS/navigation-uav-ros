# Project : Localization and detection of landmarks for supporting UAV navigation

Bachelor semester project 2: part1

## Visualizing data with ROS

1. install ROS, understanding topic, publishers and subscribers

2. Rviz tool with http://www.cvlibs.net/datasets/kitti/raw_data.php

3. Implement nodes from prerecorded rosbag containing images, localization and other sensor data and display nodes in a more advanced way.

### ros

<img src="media/ROS_diagram_1.png" width="1080">
          
<img src="media/pyramid_rock.jpg" width="1080">
 
<img src="media/new_save.png" width="1080">


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

catkin_make

source devel/setup.bash

```
### install Package : 

vision_opencv : http://wiki.ros.org/vision_opencv

cv_camera : http://wiki.ros.org/cv_camera


### launch nodes :

```
roslaunch image node.launch
```
```
roslaunch image image.launch
```
```
roslaunch image threshold.launch
```
```
roslaunch image target.launch
```
```
roslaunch image target.launch
```
```
roslaunch image target.launch
```
```
roslaunch video video.launch

```
```
roslaunch video webcam.launch
```

