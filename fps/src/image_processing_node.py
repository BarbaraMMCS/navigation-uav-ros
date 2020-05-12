#!/usr/bin/env python

#node B

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

bridge = CvBridge()


def publisher():
    pub = rospy.Publisher("/image_processed", Image, queue_size=10)
    rate = rospy.Rate(5)
    rospy.loginfo("image_processing_node is publishing to /image_processed")

    while cap.isOpened():
        _, frame = cap.read()
        image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        pub.publish(image)
        rate.sleep()
    cap.release()


def callback(data):
    image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

    cv2.imshow("image_processing_node", image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def listener():
    rospy.Subscriber("/cv_camera_node/image_raw", Image, callback)
    rospy.loginfo("image_processing_node is sunscribing to /cv_camera_node/image_raw")
    rospy.loginfo("-------------------node (B) is sunscribing to topic from node (A)")


def main():
    rospy.init_node("image_processing_node", anonymous=True)
    listener()
    publisher()
    rospy.spin()


if __name__ == '__main__':
    main()



