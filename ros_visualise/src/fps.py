#!/usr/bin/env python

# video subscriber node b

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image



class Filter:

    def __init__(self, src=0):
        self.bridge = CvBridge()
        

    def nothing(self, x):
        pass



    def callback(self, data):
        try:
            frame = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)

        cv2.namedWindow("video")

        cv2.createTrackbar("Bilateral", "video", 0, 1, self.nothing)
        while (True):
        

            # Switch bilateral blur
            switch = cv2.getTrackbarPos("Bilateral", "video")
            if switch == 0:
                pass
            else:
                frame = cv2.bilateralFilter(frame, 15, 75, 75)

            cv2.imshow("video", frame)

            if cv2.waitKey(15) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

            cv2.imshow("video", frame)

            if cv2.waitKey(15) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        

cf = None
run = Filter()


def callback(data):
    run.callback(data)    



def listener():
    rospy.Subscriber('/gray', Image, callback)
    rospy.loginfo("Subscriber is starting")



def main():
    rospy.init_node("fps", anonymous=True)

    while not rospy.is_shutdown():
        data = rospy.wait_for_message('/gray', Image)
        listener()
        rospy.spin()




if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:

        pass

