#!/usr/bin/env python

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

video_path = "/home/barbara/Videos/Drone/DJI_0004.MOV"
bridge = CvBridge()
cap = cv2.VideoCapture(video_path)


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


def callback(data):
    image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

    cv2.imshow("video", image)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def listener():
    rospy.Subscriber("/image_raw", Image, callback)
    rospy.loginfo("Subscriber is starting")


def main():
    rospy.init_node("video", anonymous=True)
    listener()
    publisher()
    rospy.spin()


if __name__ == '__main__':
    main()

