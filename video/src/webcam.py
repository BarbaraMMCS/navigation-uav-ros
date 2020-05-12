#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError


rospy.init_node("webcam", anonymous=True)
bridge = CvBridge()
topic = "/cv_camera_node/image_raw"


def callback(msg):
    rospy.loginfo("subscribing to ", topic)

    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "passthrough")
    except CvBridgeError as error:
        print(error)

    cv2.imshow("Image Window", cv_image)
    cv2.waitKey(3)


sub_image = rospy.Subscriber(topic, Image, callback)
cv2.namedWindow("Image Window", 1)

while not rospy.is_shutdown():
    rospy.spin()
