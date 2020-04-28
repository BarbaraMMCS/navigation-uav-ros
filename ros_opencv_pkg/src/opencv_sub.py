#!/usr/bin/env python

import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


bridge = CvBridge()


def callback(data):
    image = bridge.imgmsg_to_cv2(data, "mono8" )
    cv2.imshow("Main window", image)
    cv2.waitKey(10)


def subscriber():
    rospy.init_node("opencv_sub", anonymous=True)
    sub = rospy.Subscriber('image_topic', Image, callback, queue_size = 1)
    rospy.spin()


if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass
