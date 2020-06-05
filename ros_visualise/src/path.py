#!/usr/bin/env python
import rospy

from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

path = Path()

def odom_cb(data):
    global path
    path.header = data.header
    pose = PoseStamped()
    pose.header = data.header
    pose.pose = data.pose.pose
    path.poses.append(pose)
    path_pub.publish(path)

rospy.init_node('path')

topic_sub = rospy.get_param('~topic_sub')
topic_pub = rospy.get_param('~topic_pub')
odom_sub = rospy.Subscriber(topic_sub, Odometry, odom_cb)
path_pub = rospy.Publisher(topic_pub, Path, queue_size=1)

if __name__ == '__main__':
    rospy.spin()
