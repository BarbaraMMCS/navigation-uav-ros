#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image

bridg e= CvBridge()
cap = cv2.VideoCapture("/home/barbara/Videos/Drone/DJI_0004.MOV")			

rospy.init_node("Node1",anonymous=True)
pub = rospy.Publisher("/image_raw",Image,queue_size=10)
rate = rospy.Rate(10)
rospy.loginfo("Publisher is starting")

while cap.isOpened():

	_,frame=cap.read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)			 
	image_ros = bridge.cv2_to_imgmsg(frame,encoding="passthrough")
	pub.publish(image_ros)
	rate.sleep()
				
	
cap.release()
	