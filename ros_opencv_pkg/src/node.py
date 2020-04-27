#!/usr/bin/env python

import rospy
from std_msg import String
from ros_opencv_pkg.msg import custom_msg


def publisher():
    pub = rospy.Publisher('message', String, queue_size=10)
    pub = rospy.Publisher('custom message', custom_msg, queue_size=10)

    rate = rospy.Rate(10)  #10HZ

    custom_msg_to_pub = custom_msg()

    counter = 0

    while not rospy.is_shutdown():
        str = "Publishing message %s" % rospy.get_time()
        custom_str = "Publishing custom message %d" % counter
        counter +=1

        custom_msg_to_pub.data = custom_str
        custom_msg_to_pub.counter = counter

        pub.publish(str)
        pub.publish(custom_str)

        rospy.loginfo(str)
        rospy.loginfo(custom_str)

        rate.sleep()


def callback_data(data):
    rospy.loginfo(rospy.get_caller_id() + "received: %s", data.data)


def callback_msg(custom_str):
    str_received = message.data
    counter_received = message.counter
    rospy.loginfo("received: %d" % counter_received)


def subscriber():
    sub = rospy.Subscriber('message', String, callback_data)
    sub = rospy.Subscriber('custom message', custom_msg, callback_msg)

    rospy.spin()



if __name__ == '__main__':
    try:
        rospy.init_node("node", anonymous= True)
        publisher()
        subscriber()
    except rospy.ROSInterruptException:
        pass
