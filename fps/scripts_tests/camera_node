#!/usr/bin/env python


import numpy as np
import cv2 as cv

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



def publisher():
    pub = rospy.Publisher("image_camera", Image, queue_size=10)
    rate = rospy.Rate(10)  # 10HZ
    rospy.loginfo("Publisher is publishing")

    while not rospy.is_shutdown():
        msg = br.cv2_to_imgmsg(data, encoding="passthrough")
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    br = CvBridge()
    data = cv.imread("/home/barbara/Pictures/pyramid_rock.jpg")
    if (data.any()):
        rospy.init_node("camera_node", anonymous=True)
        publisher()
    else:
        print("Could not open image")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

cv.destroyAllWindows()
