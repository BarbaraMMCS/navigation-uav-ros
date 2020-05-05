#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np


def subscriber():
    rospy.Subscriber("image", Image, callback, queue_size=1)
    rospy.loginfo("Subscriber is listening")	
	

def callback(data):
   data = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
   cv2.imshow("Image", data_img)
   if cv2.waitKey(25) & 0xFF == ord('q'):
	cv2.destroyAllWindows()



def publisher():
    pub = rospy.Publisher("image", Image, queue_size=1)
    rate = rospy.Rate(10)  #10HZ
    rospy.loginfo("Publisher is publishing")		

    while not rospy.is_shutdown():
        msg = bridge.cv2_to_imgmsg(data, encoding="passthrough")
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':

    try:
        bridge = CvBridge()
        data = cv2.imread("/home/barbara/Pictures/pyramid_rock.jpg")

        rospy.init_node("image", anonymous= True)
        subscriber()
        publisher()
        rospy.spin()

    except KeyboardInterrupt:
        print("Shutting down")

    cv2.destroyAllWindows()
