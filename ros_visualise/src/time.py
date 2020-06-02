#!/usr/bin/env python

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import cv2
import imutils

def nothing(x):
    pass


def show(data):
    data = to_cv2(data)
    cv2.imshow("fps_control", imutils.resize(data, height=480))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def to_cv2(data):
    try:
        data = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    except CvBridgeError as e:
        print(e)
    return data


def slider():
    fps = float(cv2.getTrackbarPos("FPS", "fps_control"))
    if fps == 0:
        fps = 1
    else:
        pass
    return fps


def callback(data):
    topic_pub = rospy.get_param('~topic_pub')
    pub = rospy.Publisher(topic_pub, Image, queue_size=1)  
    fps = slider()
    frame_time = rospy.Duration(1/fps)
    begin_time = rospy.Time.now()
    end_time = frame_time + begin_time
    el = end_time - begin_time
    while (rospy.Time.now() < end_time):
        pub.publish(data)
        show(data)
        rospy.sleep(frame_time)


def subscriber():
    topic = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic, Image, callback)


def main():
    rospy.init_node('time')
    cv2.namedWindow("fps_control")
    fps_param = rospy.get_param('~fps')
    cv2.createTrackbar("FPS", "fps_control", fps_param, 30, nothing)
    subscriber()
    rospy.spin()


if __name__ == '__main__':
    bridge = CvBridge()
    try:
        main()
    except rospy.ROSInterruptException:
        pass
