#!/usr/bin/env python

#node B

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
    topic = "/image_processed"
    pub = rospy.Publisher(topic, Image, queue_size=10)
    rospy.loginfo("Publisher is starting")

    # starts video
    # Load file
    cap = cv2.VideoCapture("/home/barbara/Videos/Drone/DJI_0004.MOV")

    # sets fps
    frame_rate = 30
    fps = frame_rate * 1000  # because 1ms * 1000 = 1s

    # frame and time counters
    total_frames = 0
    prev = 0

    # Create window with sliders
    cv2.namedWindow("video")
    cv2.createTrackbar("FPS", "video", frame_rate, 60, nothing)
    cv2.createTrackbar("Gray", "video", 0, 1, nothing)
    cv2.createTrackbar("Bilateral", "video", 0, 1, nothing)

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

                # Resize frame
                width = 1080
                height = 720
                dim = (width, height)
                frame = cv2.resize(frame, dim, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

                # update counter, get new fps, sets new fps value
                total_frames += 1
                fps = cv2.getTrackbarPos("FPS", "video")
                frame_rate = fps

                # print on window
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, str(topic), (50, 70), font, 1, (255, 240, 200), 1)

                # Switch Gray
                switch_gray = cv2.getTrackbarPos("Gray", "video")
                if switch_gray == 0:
                    pass
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Switch Blur
                switch_bilateral = cv2.getTrackbarPos("Bilateral", "video")
                if switch_bilateral == 0:
                    pass
                else:
                    frame = cv2.bilateralFilter(frame, 15, 75, 75)

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
    rospy.Subscriber("/usb_cam/image_raw", Image, callback)
    rospy.loginfo("Subscriber is starting")
    rospy.loginfo("camera_node is subscribing to /usb_cam/image_raw")


def callback(data):
    # callback of listener
    # converts ros msg to cv2 image
    frame = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    rospy.loginfo("Showing frame from /camera")

    # shows window with frames received
    cv2.imshow("camera", frame)

    # release and destroy all windows
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def main():
    # initiate node, calls subscriber then publisher
    rospy.init_node("image_processing_node", anonymous=True)
    listener()
    publisher()
    rospy.spin()


if __name__ == '__main__':
    main()
