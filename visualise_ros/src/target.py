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
    except CvBridgeError as error:
        print(error)

    def nothing(x):
        pass

    # Image size
    shape = img.shape
    print(shape)

    # RGB colors
    white_rgb = (255, 255, 255)
    blue_rgb = (255, 0, 0)
    red_rgb = (0, 0, 255)
    green_rgb = (0, 255, 0)
    violet_rgb = (170, 0, 170)
    yellow_rgb = (0, 170, 170)

    while True:
        # Shapes
        cv.line(img, (3200, 2000), (4200, 2000), blue_rgb, 2)
        cv.circle(img, (3700, 1750), 10, red_rgb, -1)
        cv.ellipse(img, (3700, 2000), (500, 300), 180, 180, 0, green_rgb, 3)
        points = np.array([[[2000, 1000], [2000, 1250], [1300, 1200], [2300, 1400]]], np.int32)
        cv.polylines(img, [points], True, yellow_rgb, thickness=2)

        # Text
        font = cv.FONT_HERSHEY_TRIPLEX
        cv.putText(img, "pyramid rock", (3200, 1600), font, 4, violet_rgb)

        # Region of interest
        # row, column, chanel = shape
        pt1 = (1200, 2200)
        pt2 = (1800, 2600)
        pt1_x, pt1_y = pt1
        pt2_x, pt2_y = pt2
        cv.rectangle(img, pt1, pt2, white_rgb, 3)
        roi = img[pt1_y:pt2_y, pt1_x:pt2_x]  # ratio is 2:3 --> [1:row, 1.5:column]

        # image resize after drawing
        width = 720
        height = 480
        dim = (width, height)
        img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
        roi = cv.resize(roi, dim, interpolation=cv.INTER_AREA)

        # window
        cv.imshow("pyramid_rock", img)
        cv.imshow("roi", roi)
        cv.waitKey(0)




if __name__ == '__main__':
    br = CvBridge()
    # cv.imread("...", 0) for greyscale
    data = cv.imread("/home/barbara/catkin_ws/src/UAV_navigation_ROS/media/pyramid_rock.jpg", 0)
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
