#!/usr/bin/env python

#node C

import cv2
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image


bridge = CvBridge()

def publisher():
    pub = rospy.Publisher("/image_processed", Image, queue_size=10)
    rate = rospy.Rate(10)
    rospy.loginfo("image_display_node is is sunscribing to /cv_camera_node/image_raw")

    while cap.isOpened():
        _, frame = cap.read()
        image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        pub.publish(image)
        rate.sleep()
    cap.release()


def main():
    rospy.init_node("image_display_node", anonymous=True)
    publisher()


if __name__ == '__main__':
    main()


