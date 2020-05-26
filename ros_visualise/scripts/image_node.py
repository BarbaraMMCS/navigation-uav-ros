#!/usr/bin/env python

# publisher subscriber node for showing images

# import numpy as np
import cv2

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

    dim = (1920, 1080)
    image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    while True:
        cv2.imshow("Image", image)
        cv2.waitKey(3)


if __name__ == '__main__':
    br = CvBridge()
    data = cv2.imread("/home/barbara/Pictures/image.jpg", 0)
    if data.any():
        rospy.init_node("image_node", anonymous=True)
        subscriber()
        publisher()
    else:
        print("Could not open image")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
