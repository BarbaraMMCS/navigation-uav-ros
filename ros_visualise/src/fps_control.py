#!/usr/bin/env python

# ros node

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import cv2
import imutils

class Fps:

    def __init__(self):
        self.bridge = CvBridge()
        self.window = "fps_control"
        self.fps_param = rospy.get_param('~fps')
        cv2.namedWindow(self.window)
        cv2.createTrackbar("FPS", self.window, self.fps_param, 30, self.nothing)

    def nothing(self, x):
        pass

    def show(self, data):
        data = self.to_cv2(data)
        cv2.imshow(self.window, imutils.resize(data, height=480))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def to_cv2(self, data):
        try:
            data = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        return data

    def update(self):
        fps = float(cv2.getTrackbarPos("FPS", self.window))
        if fps == 0:
            fps = 1
        else:
            pass
        return fps

    def callback(self, data):
        topic_pub = rospy.get_param('~topic_pub')
        pub = rospy.Publisher(topic_pub, Image, queue_size=1)

        fps = self.update()
        frame_time = rospy.Duration(1/fps)
        begin_time = rospy.Time.now()
        end_time = frame_time + begin_time
        while rospy.Time.now() < end_time:
            pub.publish(data)
            self.show(data)
            rospy.sleep(frame_time)

    def subscriber(self):
        topic = rospy.get_param('~topic_sub')
        rospy.Subscriber(topic, Image, self.callback)


def main():
    rospy.init_node('fps_control')
    fps = Fps()
    fps.subscriber()
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
