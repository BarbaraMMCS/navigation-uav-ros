#!/usr/bin/env python

# simple publisher subcriber test

import rospy
from std_msgs.msg import String


def publisher():
    pub = rospy.Publisher('message', String, queue_size=10)
    rate = rospy.Rate(10)  #10HZ

    while not rospy.is_shutdown():
        str = "Time: %s" % rospy.get_time()
        pub.publish(str)
        rospy.loginfo(str)
        rate.sleep()


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "   received: %s", data.data)


def subscriber():
    sub = rospy.Subscriber('message', String, callback)



if __name__ == '__main__':
    try:
        rospy.init_node("node", anonymous= True)
        subscriber()
        publisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass