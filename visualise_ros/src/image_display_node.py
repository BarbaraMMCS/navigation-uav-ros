#!/usr/bin/env python

#node C

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np
import time

bridge = CvBridge()


def listener():
    #subscribe to topic and log message
    rospy.Subscriber("/image_processed", Image, callback)
    rospy.loginfo("Subscriber is starting")
    rospy.loginfo("camera_node is subscribing to /image_processed")


def callback(data):
    # callback of listener
    # converts ros msg to cv2 image
    frame = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    rospy.loginfo("Showing frame from /image_processed")

    # shows window with frames received
    cv2.imshow("video", frame)

    # release and destroy all windows
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def main():
    #initiate node, calls subscriber then publisher
    rospy.init_node("image_display_node", anonymous=True)
    listener()
    rospy.spin()


if __name__ == '__main__':
    main()
