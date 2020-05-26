#!/usr/bin/env python

# subscribes to image topic, then process image with filters, then publishes to topic

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()


def subscriber():
    topic_sub = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic_sub, Image, callback)


def callback(img):
    # conversion to cv2
    try:
        cv2_img = bridge.imgmsg_to_cv2(img, desired_encoding="passthrough")
    except CvBridgeError as error:
        print(error)

    # image to grayscale
    frame = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

    # conversion to sensor_msgs.msg.Image
    try:
        img_msg = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
    except CvBridgeError as error:
        print(error)
    # publish
    topic_pub = rospy.get_param('~topic_pub')
    pub = rospy.Publisher(topic_pub, Image, queue_size=10)
    rospy.loginfo_once("Publisher is starting")
    pub.publish(img_msg)


def main():
    rospy.init_node("process_cv2", anonymous=True)
    subscriber()
    while not rospy.is_shutdown():
        rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass