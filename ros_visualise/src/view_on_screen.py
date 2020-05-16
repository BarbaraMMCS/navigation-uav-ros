#!/usr/bin/env python

# video subscriber node b

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
    rospy.Subscriber('topic_name', Image, callback)
    rospy.loginfo("Subscriber is starting")


def main():
    rospy.init_node("view_on_screen", anonymous=True)
    listener()
    while not rospy.is_shutdown():
        rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
