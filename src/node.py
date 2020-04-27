import sys
import cv2
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
import numpy as np


class cvBridgeDemo():
    def __init__(self):
        self.node_name = "node"
        # Initialize the ros node
        rospy.init_node(self.node_name)
        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)
        # Create the cv_bridge object
        self.bridge = CvBridge()
        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)

        # Callback executed when the timer timeout
        rospy.Timer(rospy.Duration(0.03), self.show_img_cb)
        rospy.loginfo("Waiting for image topics...")

    def show_img_cb(self, event):
        try:
            cv2.namedWindow("RGB_Image", cv2.WINDOW_NORMAL)
            cv2.moveWindow("RGB_Image", 25, 75)
            cv2.namedWindow("Processed_Image", cv2.WINDOW_NORMAL)
            cv2.moveWindow("Processed_Image", 500, 75)
            cv2.waitKey(3)
        except:
            pass

    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            self.frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")

        except CvBridgeError:
            print('error')
        pass

        # Convert the image to a Numpy array since most cv2 functions
        # require Numpy arrays.
        frame = np.array(self.frame, dtype=np.uint8)
        # Process the frame using the process_image() function
        self.display_image = self.process_image(frame)

    def process_image(self, frame):
        # Convert to grayscale
        grey = cv2.cvtColor(frame, cv2.CV_BGR2GRAY)
        # Blur the image
        grey = cv2.blur(grey, (7, 7))
        # Compute edges using the Canny edge filter
        edges = cv2.Canny(grey, 15.0, 30.0)
        return edges

    def cleanup(self):
        print("Shutting down vision node.")
        cv2.destroyAllWindows()

    def main(args):
        try:
            cvBridgeDemo()
        rospy.spin()
        except KeyboardInterrupt:
        print("Shutting down vision node.")
        cv2.DestroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)



