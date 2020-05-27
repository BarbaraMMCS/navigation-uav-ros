#!/usr/bin/env python

# video subscriber node c

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

 
class Fps:

    def __init__(self):
        self.bridge = CvBridge()
	self.start = None
	self.end = None
	self.numFrames = 0
        self.fps = 30
        cv2.namedWindow("fps_sp")
        cv2.createTrackbar("fps", "fps_sp", self.fps, 30, self.nothing)

    def nothing(self, x):
        pass



    def show(self, frame):
        fps = cv2.getTrackbarPos("fps", "fps_sp")
        cv2.imshow("fps_sp", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        return fps

    def callback(self, data):

        try:
            data = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)

        if data.any():
            fps = self.show(data)

            try:
                data = self.bridge.cv2_to_imgmsg(data, encoding="passthrough")
            except CvBridgeError as error:
                print(error)
            
            rate = rospy.Rate(fps)
            topic_pub = rospy.get_param('~topic_pub')
            pub = rospy.Publisher(topic_pub, Image, queue_size=10)
            rospy.loginfo_once("Publisher is sending data")
            pub.publish(data)
            rate.sleep()
        else:
            pass


def callback(data):
    fps.callback(data)


def subscriber():
    topic = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic, Image, callback)


def main():
    rospy.init_node("fps_sp", anonymous=True)
    while not rospy.is_shutdown():
        subscriber()

        rospy.spin()


if __name__ == '__main__':
    fps = Fps()
    try:
        main()
    except rospy.ROSInterruptException:
        pass
