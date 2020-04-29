#!/usr/bin/env python

import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image


def callback(data):
    capture = cv2.VideoCapture(0)


    while capture.isOpened():
        # captures the frame
        ret, frame = capture.read()

        if ret == True:

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Because hsv is easier to deal with
         
            # color filter
            # Gray filter
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            # Show windows
            cv2.imshow("Color", frame)
            cv2.imshow("Gray", gray)


            if cv2.waitKey(1) & 0xFF == ord("q"):
                # quit key
                break
        else:
            break

    capture.release()
    output.release()
    cv2.destroyAllWindows()


def subscriber():
    rospy.init_node("opencv_sub", anonymous=True)
    sub = rospy.Subscriber('usb_cam/image_raw', Image, callback, queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass
