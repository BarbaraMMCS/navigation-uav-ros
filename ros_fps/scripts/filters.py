#!/usr/bin/env python

# video subscriber node b

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class Filter:

    def __init__(self):
        self.bridge = CvBridge()
        cv2.namedWindow("filters")
        cv2.createTrackbar("Threshold", "filters", 128, 255, self.nothing)
        cv2.createTrackbar("Gray", "filters", 1, 1, self.nothing)

    def nothing(self, x):
        pass

    def filter(self, data):
        value_th = cv2.getTrackbarPos("Threshold", "filters")
        _, data = cv2.threshold(data, value_th, 255, cv2.THRESH_TRUNC)
        switch_gray = cv2.getTrackbarPos("Gray", "filters")
        if switch_gray == 0:
            pass
        else:
            data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        cv2.imshow("filters", data)
        if cv2.waitKey(15) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        return data

    def callback(self, data):
        try:
            data = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        if data.any():
            data = self.filter(data)
            try:
                data = self.bridge.cv2_to_imgmsg(data, encoding="passthrough")
            except CvBridgeError as error:
                print(error)
            topic_pub = rospy.get_param('~topic_pub')
            pub = rospy.Publisher(topic_pub, Image, queue_size=10)
            rospy.loginfo_once("Publisher is sending data")
            pub.publish(data)
        else:
            pass


def callback(data):
    image.callback(data)


def subscriber():
    topic = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic, Image, callback)
    rospy.loginfo("Subscriber is starting")


def main():
    rospy.init_node("filters", anonymous=True)
    while not rospy.is_shutdown():
        subscriber()
        rospy.spin()


if __name__ == '__main__':
    image = Filter()
    try:
        main()
    except rospy.ROSInterruptException:
        pass
