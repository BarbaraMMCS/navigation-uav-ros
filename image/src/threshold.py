#!/usr/bin/env python

"""
description
usage example
parameters
"""

import numpy as np
import cv2 as cv

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

        # image resize
        width = 1920 / 2
        height = 1080 / 2
        dim = (width, height)
        image = cv.resize(img, dim, interpolation=cv.INTER_AREA)

        # Gray filter
        # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Red filter
        # hsv_frame = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # low_red = np.array([161, 155, 84])
        # high_red = np.array([179, 255, 255])
        # red_mask = cv.inRange(hsv_frame, low_red, high_red)
        # red = cv.bitwise_and(img, img, mask=red_mask)

        def nothing(x):
            pass

        # slider
        cv.namedWindow("Image")
        cv.createTrackbar("value", "Image", 128, 255, nothing)

        while True:
            # slider value tracker
            value_th = cv.getTrackbarPos("value", "Image")

            # filters
            _, th_binary = cv.threshold(image, value_th, 255, cv.THRESH_BINARY)
            _, th_binary_inv = cv.threshold(image, value_th, 255, cv.THRESH_BINARY_INV)
            _, th_trunc = cv.threshold(image, value_th, 255, cv.THRESH_TRUNC)
            _, th_to_zero = cv.threshold(image, value_th, 255, cv.THRESH_TOZERO)
            _, th_to_zero_inv = cv.threshold(image, value_th, 255, cv.THRESH_TOZERO_INV)

            # Show window
            cv.imshow("th_binary", th_binary)
            cv.imshow("th_binary_inv", th_binary_inv)
            cv.imshow("th_to_zero", th_to_zero)
            cv.imshow("th_to_zero_inv", th_to_zero_inv)
            cv.imshow("th_trunc", th_trunc)
            cv.imshow("Image", image)
            # cv.imshow("Gray", gray)
            # cv.imshow("Red", red)

            cv.waitKey(0)

    except CvBridgeError as error:
        print(error)


if __name__ == '__main__':
    br = CvBridge()
    # cv.imread("...", 0) for greyscale
    data = cv.imread("/home/barbara/catkin_ws/src/UAV_navigation_ROS/media/pyramid_rock.jpg")
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
