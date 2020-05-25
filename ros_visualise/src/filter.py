#!/usr/bin/env python

# video subscriber node b

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class Filter:

    def __init__(self, src=0):
        self.bridge = CvBridge()

    def nothing(self, x):
        pass

    def filter(self, frame):

        cv2.namedWindow("video")
        cv2.createTrackbar("value", "video", 128, 255, self.nothing)
        while True:
            value_th = cv2.getTrackbarPos("value", "video")
            _, th_trunc = cv2.threshold(frame, value_th, 255, cv2.THRESH_TRUNC)

            cv2.imshow("th_trunc", th_trunc)
            cv2.imshow("video", frame)

            if cv2.waitKey(15) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

    def callback(self, data):
        try:
            frame = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)

        self.filter(frame)


cf = None
run = Filter()


def callback(data):
    run.callback(data)


def listener():
    rospy.Subscriber('/gray', Image, callback)
    rospy.loginfo("Subscriber is starting")


def main():
    rospy.init_node("filter", anonymous=True)

    while not rospy.is_shutdown():
        data = rospy.wait_for_message('/gray', Image)
        listener()
        rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:

        pass
