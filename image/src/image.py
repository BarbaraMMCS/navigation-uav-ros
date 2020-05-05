#!/usr/bin/env python

"""
description
usage example
parameters
"""

import numpy as np
import cv2 as cv

import sys

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



def subscriber():
    rospy.Subscriber("image", Image, callback, queue_size=1)
    rospy.loginfo("Subscriber is listening")


def publisher():
    pub = rospy.Publisher("image", Image, queue_size=10)
    rate = rospy.Rate(10)  # 10HZ
    rospy.loginfo("Publisher is publishing")

    while not rospy.is_shutdown():
        msg = br.cv2_to_imgmsg(data, encoding="passthrough")
        pub.publish(msg)
        rate.sleep()


def callback(data):
    try:
        img = br.imgmsg_to_cv2(data, desired_encoding="passthrough")
    except CvBridgeError as error:
        print(error)
    cv.imshow("image", img)
    cv.waitKey(0)



if __name__ == '__main__':
    br = CvBridge()
    data = cv.imread("/home/barbara/Pictures/pyramid_rock.jpg")
    if (data.any()):
        rospy.init_node("image", anonymous=True)
        subscriber()
        publisher()
    else:
        print("Could not open image")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

    cv.destroyAllWindows()

