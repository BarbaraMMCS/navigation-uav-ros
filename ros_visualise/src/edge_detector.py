#!/usr/bin/env python

# video subscriber node d

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import imutils

class Edge:

    def __init__(self):
        self.bridge = CvBridge()
        self.min_val = 200
        self.max_val = 300
        self.aperture_size = 3
        self.gray = None
        self.window = "edge_detector"
        cv2.namedWindow(self.window)
        cv2.createTrackbar('Min', self.window, 0, 800, self.min_change)
        cv2.createTrackbar('Max', self.window, 100, 800, self.max_change)

    def change_params(self, name, value):
        self.edge_params = value
        print(self.edge_params)
        redraw_edges()

    def redraw_edges(self):
        edges = cv2.Canny(self.gray, self.min_val, self.max_val, self.aperture_size)
        self.show(edges)

    def min_change(self, new_val):
        self.min_val = new_val

    def max_change(self, new_val):
        self.max_val = new_val

    def edge(self, data):
        self.gray = data
        self.redraw_edges()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        return data

    def show(self, data, wait=1):
        cv2.imshow(self.window, imutils.resize(data, height=480))
        if cv2.waitKey(wait) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

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

    def callback(self, data):
        data = self.to_cv2(data)
        if data.any():
            data = self.edge(data)
            data = self.to_imgmsg(data)
            topic_pub = rospy.get_param('~topic_pub')
            pub = rospy.Publisher(topic_pub, Image, queue_size=10)
            pub.publish(data)
        else:
            pass


def callback(data):
    image.callback(data)


def subscriber():
    topic = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic, Image, callback)


def main():
    rospy.init_node("edge_detector", anonymous=True)
    while not rospy.is_shutdown():
        subscriber()
        rospy.spin()


if __name__ == '__main__':
    image = Edge()
    try:
        main()
    except rospy.ROSInterruptException:
        pass
