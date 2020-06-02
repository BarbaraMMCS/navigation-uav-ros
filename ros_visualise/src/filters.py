#!/usr/bin/env python

# ros node

import rospy
import cv2
import imutils
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class Filter:

    def __init__(self):
        self.bridge = CvBridge()
        self.window = "filters"
        cv2.namedWindow(self.window)
        self.sliders("Threshold", a=128, b=255)
        self.sliders("Gray")

        # slider and callback
    def sliders(self, name, a=1, b=1, window=None, call=None):
        if window is None:
            window = self.window
        if call is None:
            call = self.nothing
        cv2.createTrackbar(name, window, a, b, call)

    def nothing(self, x):
        pass

        # filters
    def filters(self, data):
        value_th = cv2.getTrackbarPos("Threshold", self.window)
        _, data = cv2.threshold(data, value_th, 255, cv2.THRESH_TRUNC)
        switch = cv2.getTrackbarPos("Gray", self.window)
        if switch == 0:
            pass
        else:
            data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        return data

        # msgs conversion
    def to_cv2(self, data, encoding="passthrough"):
        try:
            data = self.bridge.imgmsg_to_cv2(data, desired_encoding=encoding)
        except CvBridgeError as e:
            print(e)
        return data

    def to_imgmsg(self, data, encoding="passthrough"):
        try:
            data = self.bridge.cv2_to_imgmsg(data, encoding=encoding)
        except CvBridgeError as e:
            print(e)
        return data

        # display data
    def show(self, data, wait=1):
        cv2.imshow(self.window, imutils.resize(data, height=480))
        if cv2.waitKey(wait) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

        # publisher
    def publisher(self, data, rate=30, queue=10):
        topic_pub = rospy.get_param('~topic_pub')
        pub = rospy.Publisher(topic_pub, Image, queue_size=queue)
        pub.publish(data)
        rate = rospy.Rate(rate)
        rate.sleep()

        # subscriber callback
    def callback(self, data):
        data = self.to_cv2(data)
        if data.any():
            data = self.filters(data)
            self.show(data)
            data = self.to_imgmsg(data)
            self.publisher(data)
        else:
            pass


def callback(data):
    image.callback(data)


def subscriber():
    topic = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic, Image, callback)


def main():
    rospy.init_node(image.window, anonymous=True)
    while not rospy.is_shutdown():
        subscriber()
        rospy.spin()


if __name__ == '__main__':
    try:
        image = Filter()
        main()
    except rospy.ROSInterruptException:
        pass
