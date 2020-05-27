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
        cv2.namedWindow("edge_detector")
        cv2.createTrackbar('Min', 'edge_detector', 0, 800, self.min_change)
        cv2.createTrackbar('Max', 'edge_detector', 100, 800, self.max_change)

    def change_params(self, name, value):
        self.edge_params = value
        print(self.edge_params)
        redraw_edges()

    def redraw_edges(self):
        edges = cv2.Canny(self.gray, self.min_val, self.max_val, self.aperture_size)
        cv2.imshow('edge_detector', imutils.resize(edges, height=480))

    def min_change(self, new_val):
        self.min_val = new_val

    def max_change(self, new_val):
        self.max_val = new_val

    def edge(self, data):
        data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        self.gray = data
        self.redraw_edges()
        #cv2.imshow("gray", data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        return data

    def callback(self, data):
        try:
            data = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        if data.any():
            data = self.edge(data)

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
