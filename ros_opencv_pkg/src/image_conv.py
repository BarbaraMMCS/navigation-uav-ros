#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def image_process(image):
    # Image size
    shape = image.shape
    print(shape)

    while True:

        # image resize
        width = 720
        height = 480
        dim = (width, height)
        img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        return img



def msg_to_numpy(data):
    raw_img = bridge.imgmsg_to_cv2(data, "bgr8")
    return raw_img


def numpy_to_msg(img):
    data = bridge.cv2_to_imgmsg(img, "bgr8")
    return data


def callback(data):
   img = msg_to_numpy(data)
   cv2.imshow("pyramid_rock", img)
   cv2.waitKey(3)


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
    raw_img = msg_to_numpy(sub)
    image_process(raw_img)

    rospy.spin()


if __name__ == '__main__':
    try:
        bridge = CvBridge()
        rospy.init_node("image", anonymous= True)
        publisher()
        subscriber()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
