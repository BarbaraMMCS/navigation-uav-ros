#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError


rospy.init_node("webcam", anonymous=True)
bridge = CvBridge()

def show_image(img):
    cv.imshow("Image Window", img)
    cv.waitKey(3)


def image_callback(img_msg):
    rospy.loginfo(img_msg.header)

    try:
        cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
    except CvBridgeError as error:
        print(error)

    show_image(cv_image)


sub_image = rospy.Subscriber("/cv_camera_node/image_raw", Image, image_callback)
cv.namedWindow("Image Window", 1)

while not rospy.is_shutdown():
    rospy.spin()
