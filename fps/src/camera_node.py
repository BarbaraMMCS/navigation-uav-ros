#!/usr/bin/env python

# roslaunch fps camera_node.launch
# to stop 'q' in window then 'Ctrl+c' in terminal

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np
import time

bridge = CvBridge()


def publisher():
    # callback nothing
    def nothing(x):
        pass

    # creates topic to publish to, and initiate it
    pub = rospy.Publisher("/image_processed", Image, queue_size=10)
    rospy.loginfo("Publisher is starting")

    # starts video
    cap = cv2.VideoCapture(0)

    # sets fps
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    fps = frame_rate * 1000  # because 1ms * 1000 = 1s

    # frame and time counters
    total_frames = 0
    prev = 0

    # Create window with sliders
    cv2.namedWindow("video")
    cv2.createTrackbar("FPS", "video", frame_rate, 60, nothing)
    cv2.createTrackbar("Gray", "video", 1, 1, nothing)
    cv2.createTrackbar("Threshold", "video", 0, 1, nothing)

    # While video run
    while cap.isOpened():

        # Time start - time of previous loop
        time_elapsed = time.time() - prev

        # Extract frame by frame
        ret, frame = cap.read()

        # Flip frame : 0 = up side down , 1 = mirror
        frame = cv2.flip(frame, 1)

        # fps calculation
        if time_elapsed > 1 / frame_rate:
            prev = time.time()

            # if frame
            if ret:

                # update counter, get new fps, sets new fps value
                total_frames += 1
                fps = cv2.getTrackbarPos("FPS", "video")
                frame_rate = fps

                # Switch Gray
                switch_gray = cv2.getTrackbarPos("Gray", "video")
                if switch_gray == 0:
                    pass
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Switch Threshold
                switch_th = cv2.getTrackbarPos("Threshold", "video")
                if switch_th == 0:
                    pass
                else:
                    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

                # stops loop
                if cv2.waitKey(fps) & 0xFF == ord("q"):  # one loop is 1ms for waitkey(1)
                    break
            else:
                break

        # publishing at slider fps
        rate = rospy.Rate(frame_rate)

        # convert image to ros msg
        image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")

        # publish image
        pub.publish(image)

        # prints message to terminal
        rospy.loginfo("camera_node is Publishing")
        rospy.loginfo("fps: {0}".format(fps))
        rospy.loginfo("time elapsed: {0}".format(time_elapsed))

        # stop
        rate.sleep()
    cap.release()


def listener():
    # subscribe to topic and log message
    rospy.Subscriber("/image_processed", Image, callback)
    rospy.loginfo("Subscriber is starting")
    rospy.loginfo("camera_node is subscribing to /image_processed")


def callback(data):
    # callback of listener
    # converts ros msg to cv2 image
    image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    rospy.loginfo("Showing frame from /image_processed")

    # shows window with frames received
    cv2.imshow("video", image)

    # release and destroy all windows
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def main():
    # initiate node, calls subscriber then publisher
    rospy.init_node("video", anonymous=True)
    listener()
    publisher()
    rospy.spin()


if __name__ == '__main__':
    main()
