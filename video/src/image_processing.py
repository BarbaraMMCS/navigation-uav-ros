#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np


bridge = CvBridge()
cap = cv2.VideoCapture("/home/barbara/Videos/Drone/DJI_0004.MOV")

def callback(data):

	data_ros = bridge.imgmsg_to_cv2(data,desired_encoding="passthrough")		
	_,frame = cap.read()		
	
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)			
			
	cv2.imshow('frame',frame)
	
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()

def listener():
	rospy.init_node("Node2",anonymous=True)
	rospy.Subscriber("/image_raw",Image,callback)	
	rospy.loginfo("Subscriber is starting")		
	rospy.spin()

if __name__=='__main__':
	listener()
