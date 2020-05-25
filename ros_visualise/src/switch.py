#!/usr/bin/env python

# video subscriber node c

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class Filter:

    def __init__(self):
        self.bridge = CvBridge()
        cv2.namedWindow("video")
        cv2.createTrackbar("Gray", "video", 0, 1, self.nothing)

    def nothing(self, x):
        pass

    def filter(self, frame):

        # Switch Gray
        switch_gray = cv2.getTrackbarPos("Gray", "video")
        if switch_gray == 0:
            pass
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        cv2.imshow("video", frame)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def callback(self, data):
        try:
            frame = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        if frame.any():
            self.filter(frame)
        else:
            pass


def callback(data):
    run.callback(data)


def listener():
    rospy.Subscriber('/gray', Image, callback)
    rospy.loginfo("Subscriber is starting")
      

def main():
    rospy.init_node("switch", anonymous=True)
    while not rospy.is_shutdown():
        data = rospy.wait_for_message('/gray', Image)
        listener()
        rospy.spin()


if __name__ == '__main__':
    run = Filter()
    try:
        main()
    except rospy.ROSInterruptException:
        pass





