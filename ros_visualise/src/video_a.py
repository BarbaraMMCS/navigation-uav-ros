#!/usr/bin/env python

# video publisher node a

import cv2
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image


bridge = CvBridge()
cap = cv2.VideoCapture(0)


def publisher():
    pub = rospy.Publisher("/image_raw", Image, queue_size=10)
    rate = rospy.Rate(10)
    rospy.loginfo("Publisher is starting")

    while cap.isOpened():
        _, frame = cap.read()
        image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        pub.publish(image)
        rate.sleep()
    cap.release()


def main():
    rospy.init_node("video_a", anonymous=True)
    publisher()


if __name__ == '__main__':
    main()
