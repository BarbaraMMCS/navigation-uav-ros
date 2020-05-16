#!/usr/bin/env python

# subscribes to image topic, then process image with filters, then publishes to topic

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError


bridge = CvBridge()


def subscriber():
    rospy.Subscriber('topic_name', Image, callback)


def callback(img):
    # conversion to cv2
    try:
        cv2_img = bridge.imgmsg_to_cv2(img, desired_encoding="passthrough")
    except CvBridgeError as error:
        print(error)

    # image to grayscale
    frame = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    
    # conversion to sensor_msgs.msg.Image
    try:
        img_msg = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
    except CvBridgeError as error:
        print(error)
    # publish 
    pub = rospy.Publisher('/gray', Image, queue_size=10)
    rospy.loginfo_once("Publisher is starting")
    pub.publish(img_msg)



def main():
    rospy.init_node("process_cv2_node", anonymous=True)
    subscriber()
    while not rospy.is_shutdown():
        rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass












import time



def fps(num):

    def nothing(x):
        pass


    fps = frame_rate
    total_frames = 0
    prev = 0

    cv2.createTrackbar("FPS", "video", frame_rate, frame_rate, nothing)

    time_elapsed = time.time() - prev
    frame = img_msg
    total_frames += 1

    if time_elapsed > 1 / frame_rate:
        prev = time.time()
        fps = cv2.getTrackbarPos("FPS", "video")
        if fps == 0:
            frame_rate = 1
        else:
            frame_rate = fps

        return

num = get fps from topic # add custom msg float
rate = rospy.Rate(fps(num))

pub.publish(image)

