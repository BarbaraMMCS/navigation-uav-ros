#!/usr/bin/env python

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import cv2


def nothing(x):
    pass


def show(data):
    data = to_cv2(data)
    cv2.imshow("video", data)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def to_cv2(data):
    try:
        data = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    except CvBridgeError as e:
        print(e)
    return data

"""
def slider():
    try: 
        fps = cv2.getTrackbarPos("FPS", "video")
    except ZeroDivisionError as b:
        print(b)
    return float(fps)
"""

def slider():
    fps = float(cv2.getTrackbarPos("FPS", "video"))
    if fps == 0:
        fps = 1
    else:
        pass
    return fps


def callback(data):
    pub = rospy.Publisher('time', Image, queue_size=1)
   
    fps = slider()
    rospy.loginfo("fps_slider: {0}".format(fps))

    frame_time = rospy.Duration(1/fps)


    begin_time = rospy.Time.now()
    end_time = frame_time + begin_time

    el = end_time - begin_time
    rospy.loginfo("elapsed: {0}".format(el.to_sec()))

    while (rospy.Time.now() < end_time):
        pub.publish(data)
        show(data)
        rospy.sleep(frame_time)


def subscriber():
    rospy.Subscriber('/usb_cam/image_raw', Image, callback)


def main():
    rospy.init_node('time')
    cv2.namedWindow("video")
    cv2.createTrackbar("FPS", "video", 25, 30, nothing)
    subscriber()
    rospy.spin()


if __name__ == '__main__':
    bridge = CvBridge()
    try:
        main()
    except rospy.ROSInterruptException:
        pass
