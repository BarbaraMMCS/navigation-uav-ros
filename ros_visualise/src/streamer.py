#!/usr/bin/env python

# ros node

import cv2
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS


class Video:

    def __init__(self):
        self.num_frames = rospy.get_param('~num_frames')
        self.display = rospy.get_param('~display')
        self.video_path = rospy.get_param('~video_path')

        self.bridge = CvBridge()
        self.vs = WebcamVideoStream(src=self.video_path).start()
        self.fps = FPS().start()

    def clean_shutdown(self):
        cv2.destroyAllWindows()
        self.vs.stop()

    def to_imgmsg(self, data, encoding="passthrough"): 
        try:
            data = self.bridge.cv2_to_imgmsg(data, encoding=encoding)
        except CvBridgeError as e:
            print(e)
        return data

    def show(self, data, wait=1):
        cv2.imshow("videofile", imutils.resize(data, height=480))
        if cv2.waitKey(wait) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def publisher(self, data):
        topic_pub = rospy.get_param('~topic_pub')
        pub = rospy.Publisher(topic_pub, Image, queue_size=10)    
        data = self.to_imgmsg(data, encoding="bgr8")
        pub.publish(data)

    def stream(self):
        while self.fps._numFrames < self.num_frames:
            frame = self.vs.read()
        if self.display > 0:
            self.show(frame)
        self.publisher(frame)
        self.fps.update()
        self.fps.stop()
        cv2.destroyAllWindows()
        self.vs.stop()


def main():
    rospy.init_node("videofile", anonymous=True)
    video = Video()
    rospy.on_shutdown(video.clean_shutdown)
    video.stream()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
