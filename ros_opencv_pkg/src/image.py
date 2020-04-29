#!/usr/bin/env python

import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def image_process(image):
    # Image size
    shape = image.shape
    print(shape)

    # RGB colors
    white_rgb = (255, 255, 255)
    blue_rgb = (255, 0, 0)
    red_rgb = (0, 0, 255)
    green_rgb = (0, 255, 0)
    violet_rgb = (170, 0, 170)
    yellow_rgb = (0, 170, 170)

    while True:

        # Shapes
        cv2.line(image, (3200, 2000), (4200, 2000), blue_rgb, 2)
        cv2.circle(image, (3700, 1750), 10, red_rgb, -1)
        cv2.ellipse(image, (3700, 2000), (500, 300), 180, 180, 0, green_rgb, 3)
        points = np.array([[[2000, 1000], [2000, 1250], [1300, 1200], [2300, 1400]]], np.int32)
        cv2.polylines(image, [points], True, yellow_rgb, thickness=2)

        # Text
        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(image, "pyramid rock", (3200, 1600), font, 4, violet_rgb)

        # Region of interest
        # row, column, chanel = shape
        pt1 = (1200, 2200)
        pt2 = (1800, 2600)
        pt1_x, pt1_y = pt1
        pt2_x, pt2_y = pt2
        cv2.rectangle(image, pt1, pt2, white_rgb, 3)
        roi = image[pt1_y:pt2_y, pt1_x:pt2_x] # ratio is 2:3 --> [1:row, 1.5:column]

        # image resize after drawing
        width = 720
        height = 480
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        roi = cv2.resize(roi, dim, interpolation=cv2.INTER_AREA)

        # window
        cv2.imshow("pyramid_rock", image)
        cv2.imshow("roi", roi)


def msg_to_numpy(data):
    raw_img = self.__bridge.imgmsg_to_cv2(data, "bgr8")
    return raw_img


def numpy_to_msg(img):     
    data = bridge.cv2_to_imgmsg(img, "rgb8")
    return data


def callback(data):
   img = msg_to_numpy(data)


def publisher():
    pub = rospy.Publisher("image_pub", Image, queue_size=1)
    rate = rospy.Rate(10)  #10HZ
    while not rospy.is_shutdown():
        image_path = "/home/barbara/Pictures/pyramid_rock.jpg"
        img = cv2.imread(image_path) 
        msg = numpy_to_msg(img)
        pub.publish(msg)
        rospy.loginfo(msg)
        rate.sleep()


def subscriber():
    sub = rospy.Subscriber("image_pub", Image, callback, queue_size=1)
    image = msg_to_numpy(sub)
    image_process(image)

    rospy.spin()


if __name__ == '__main__':
    try:
        bridge = CvBridge()
        rospy.init_node("image", anonymous= True)
        publisher()
        subscriber()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
    	pass
    cv2.destroyAllWindows()





