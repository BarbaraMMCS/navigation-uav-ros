#!/usr/bin/env python
import cv2
import rospy
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
from mydia import Videos


video_path = "/home/barbara/Videos/Drone/DJI_0004.MOV"
bridge= CvBridge()
cap = cv2.VideoCapture(video_path)			


def publisher():

    pub = rospy.Publisher("/image_raw", Image, queue_size=10)
    rate = rospy.Rate(10)
    rospy.loginfo("Publisher is starting")

    while cap.isOpened():

	_,frame=cap.read()
	image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
	pub.publish(image)
	rate.sleep()
				
    cap.release()


def callback(data):

    image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    _,frame = cap.read()		

    cv2.imshow('frame', frame)
	
    if cv2.waitKey(25) & 0xFF == ord('q'):
	cv2.destroyAllWindows()


def listener():
    rospy.Subscriber("/image_raw", Image, callback)
    rospy.loginfo("Subscriber is starting")
		
    reader = Videos(num_frames=120, mode=select_frames)
    video = reader.read(video_path)  # A video tensor/array


def select_frames(total_frames, num_frames, fps, *args):
    """This function will return the indices of the frames to be captured"""
    N = 1
    t = np.arange(total_frames)
    f = np.arange(num_frames)
    mask = np.resize(f, total_frames)

    return t[mask < N][:num_frames].tolist()

   # Let's assume that the duration of your video is 120 seconds
   # and you want 1 frame for each second 
   # (therefore, setting `num_frames` to 120)



def main():
    rospy.init_node("video", anonymous=True)
    listener()
    publisher()
    rospy.spin()

if __name__=='__main__':
	main()
	
