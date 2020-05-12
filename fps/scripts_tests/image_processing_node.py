#!/usr/bin/env python


import numpy as np
import cv2 
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



def main():
    sub = rospy.Subscriber("image_camera", Image, callback, queue_size=1)
    pub = rospy.Publisher("image_processed", Image, queue_size=10)


def callback(data):
    rospy.loginfo("image_processing_node is listening")
    cv_image = br.imgmsg_to_cv2(data, desired_encoding="passthrough")
    msg = br.cv2_to_imgmsg(cv_image, encoding="passthrough") 
    pub.publish(msg)
    rospy.loginfo("image_processing_node is publishing")



if __name__ == '__main__':
    br = CvBridge()
    rospy.init_node("image_processing_node", anonymous=True)
    main()
    rospy.spin()





