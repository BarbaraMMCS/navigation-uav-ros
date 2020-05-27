#!/usr/bin/env python

# video publisher node a

import cv2
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image



class node:
    
    def __init__(self):
        self.start = rospy.Time.now()
        self.stop = rospy.Time.now()
        self.num_frames = 30
        self.bridge = CvBridge()

        cv2.namedWindow("fps")
        cv2.createTrackbar("fps", "fps", 10, 30, self.nothing)

    def nothing(self, x):
        pass

    def timer_start(self):
        self.start = rospy.Time.now()
        return self
    
    def timer_stop(self):
        self.stop = rospy.Time.now()
        
    def update(self):
        self.numFrames = int(cv2.getTrackbarPos("fps", "fps"))
        
    def elapsed(self):
        return (self.stop - self.start)
    
    def fps(self):
        return self.numFrames / self.elapsed()

    def to_cv2(self, data):
        try:
            data = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        return data

    def to_rosmsg(self, data):
        try:
            data = data = self.bridge.cv2_to_imgmsg(data, encoding="passthrough")
        except CvBridgeError as e:
            print(e)
        return data

    def show(self, data):
        cv2.imshow("fps", data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def publisher(self, data, fps):
        data = self.to_rosmsg(data)
        rate = rospy.Rate(fps)
        topic_pub = rospy.get_param('~topic_pub')
        pub = rospy.Publisher(topic_pub, Image, queue_size=10)
        pub.publish(data)
        rate.sleep()


    def callback(self, data):    
        duration = self.time_elapsed()
        frames = self.num_frames
        if duration > 1/ frames:
            self.timer_start
        data = self.to_cv2(data)     
        if data.any():
            self.update()
            self.show(data)
            fps = self.fps()
            self.publisher(data, fps)
        else:
            pass


def callback(data):
    node.callback(data)
    print("[INFO] elasped time: {:.2f}".format(node.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(node.fps()))


def subscriber():
    topic_sub = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic_sub, Image, callback)


def main():

    while not rospy.is_shutdown():
        subscriber()
        rospy.spin()


if __name__ == '__main__':
    rospy.init_node("test", anonymous=True)
    node = node()
    try:
        main()
    except rospy.ROSInterruptException:
        pass
