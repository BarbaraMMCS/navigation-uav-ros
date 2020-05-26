#!/usr/bin/env python

# node b

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError


bridge = CvBridge()


def subscriber():
    rospy.Subscriber('/usb_cam/image_raw', Image, callback)


def callback(img):

    # publish 
    pub = rospy.Publisher('/gray', Image, queue_size=10)
    rospy.loginfo_once("Publisher is starting")
    pub.publish(img)



def main():
    rospy.init_node("img_publisher", anonymous=True)

    while not rospy.is_shutdown():
        subscriber()
        rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
