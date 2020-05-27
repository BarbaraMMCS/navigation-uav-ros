#!/usr/bin/env python

# video publisher node a

import cv2
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image



class node:
    
    def __init__(self, fps):
        self.start = rospy.Time.now()
        self.stop = rospy.Time.now()
        self.fps = fps
        self.num_frames = 0
        self.bridge = CvBridge()

        cv2.namedWindow("fps")
        cv2.createTrackbar("fps", "fps", self.fps, 30, self.nothing)

    def nothing(self, x):
        pass

    def timer_start(self):
        self.start = rospy.Time.now()
        return self
    
    def timer_stop(self):
        self.stop = rospy.Time.now()
        
    def update(self):
        self.fps = int(cv2.getTrackbarPos("fps", "fps"))

    def elapsed(self):
        return (self.stop - self.start)
    
    def fps(self):
        return self.num_frames / self.elapsed().secs

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
        rate = rospy.Rate(self.fps)
        topic_pub = rospy.get_param('~topic_pub')
        pub = rospy.Publisher(topic_pub, Image, queue_size=10)
        pub.publish(data)
        rospy.loginfo("fps: {0}".format(self.fps))
        rospy.loginfo("time elapsed: {0}".format(self.elapsed()))
        rate.sleep()


    def callback(self, data):    
        print('start', self.start.secs)
        print('stop', self.stop.secs)
        print('num_frames', self.num_frames)
        print('elapsed', self.elapsed())
        print('fps', self.fps)

        data = self.to_cv2(data)     
        if data.any():
            self.timer_start()
            self.show(data)
            self.update()
            fps = self.fps
            self.publisher(data, fps)
        else:
            pass



def callback(data):
    node.num_frames += 1
    node.callback(data)
    node.timer_stop()

def subscriber():
    topic_sub = rospy.get_param('~topic_sub')
    rospy.Subscriber(topic_sub, Image, callback)


def main():
    fps = rospy.get_param('~fps')
    while not rospy.is_shutdown():
        subscriber()
        rospy.spin()


if __name__ == '__main__':
    rospy.init_node("test", anonymous=True)
    fps = rospy.get_param('~fps')
    node = node(fps)
    try:
        main()
    except rospy.ROSInterruptException:
        pass
