#!/usr/bin/env python

# study of one node, captures video from webcam or file
# publishes processed frames at fps slider value to a topic
# subscribes to this same topic and shows frame in a window
# does not Ctrl ^c propely, can be imporved

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
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('file.mov')

    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    fps = frame_rate
    total_frames = 0
    prev = 0

    cv2.namedWindow("video_node")
    cv2.createTrackbar("FPS", "video", frame_rate, frame_rate, nothing)
    cv2.createTrackbar("Gray", "video", 1, 1, nothing)

    while cap.isOpened():
        time_elapsed = time.time() - prev
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if time_elapsed > 1 / frame_rate:
            prev = time.time()
            if ret:
                total_frames += 1
                # Fps slider
                fps = cv2.getTrackbarPos("FPS", "video")
                if fps == 0:
                    fps = 1
                else:
                    frame_rate = fps
                # Switch Gray
                switch_gray = cv2.getTrackbarPos("Gray", "video")
                if switch_gray == 0:
                    pass
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        try:
            image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        except CvBridgeError as error:
            print(error)

        rate = rospy.Rate(frame_rate)
        pub.publish(image)
        rospy.loginfo("camera_node is Publishing")
        rospy.loginfo("fps: {0}".format(fps))
        rospy.loginfo("time elapsed: {0}".format(time_elapsed))
        rate.sleep()
    cap.release()


def subscriber():
    rospy.Subscriber("/image_processed", Image, callback)
    rospy.loginfo("Subscriber is starting")
    rospy.loginfo("camera_node is subscribing to /image_processed")


def callback(data):
    try:
        image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    except CvBridgeError as error:
        print(error)

    rospy.loginfo("Showing frame from /image_processed")

    cv2.imshow("video", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def main():
    # initiate node, calls subscriber, publisher
    rospy.init_node("video_node", anonymous=True)
    subscriber()
    publisher()
    rospy.spin()


if __name__ == '__main__':
    main()
