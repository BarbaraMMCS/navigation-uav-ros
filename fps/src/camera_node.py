#!/usr/bin/env python

# rosrun fps camera_node.py

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np
import time

bridge = CvBridge()

def publisher():

    def nothing(x):
        pass

    pub = rospy.Publisher("/image_processed", Image, queue_size=10)
    rospy.loginfo("Publisher is starting")

    frame_rate = 30
    fps = frame_rate * 1000
    total_frames = 0
    prev = 0

    cv2.namedWindow("video")
    cv2.createTrackbar("FPS", "video", frame_rate, 60, nothing)
    cv2.createTrackbar("Gray", "video", 0, 1, nothing)

    video_path = 0
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():

        time_elapsed = time.time() - prev
        ret, frame = cap.read()
        if time_elapsed > 1 / frame_rate:
            prev = time.time()
            if ret:
                total_frames += 1
                fps = cv2.getTrackbarPos("FPS", "video")
                frame_rate = fps

                # Switch Gray
                switch_gray = cv2.getTrackbarPos("Gray", "video")
                if switch_gray == 0:
                    pass
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if cv2.waitKey(fps) & 0xFF == ord("q"):
                    break
            else:
                break
        rate = rospy.Rate(frame_rate)
        image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        pub.publish(image)
        rospy.loginfo("camera_node is Publishing")
        rate.sleep()
    cap.release()


def listener():
    rospy.Subscriber("/image_processed", Image, callback)
    rospy.loginfo("Subscriber is starting")
    rospy.loginfo("camera_node is subscribing to /image_processed")


def callback(data):
    image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    rospy.loginfo("callback is showing frame from /image_processed")
    cv2.imshow("video", image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def main():
    rospy.init_node("video", anonymous=True)
    listener()
    publisher()
    rospy.spin()


if __name__ == '__main__':
    main()
