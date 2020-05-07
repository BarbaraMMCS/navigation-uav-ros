#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge()


def callback(data):
    image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

    cv2.imshow("video", image)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def listener():
    rospy.init_node("image_processing", anonymous=True)
    rospy.Subscriber("/image_raw", Image, callback)
    rospy.loginfo("Subscriber is starting")
    rospy.spin()


if __name__ == '__main__':
    listener()