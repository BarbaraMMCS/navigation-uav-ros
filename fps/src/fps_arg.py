#!/usr/bin/env python

# rosrun fps fps_arg.py

import argparse
import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

bridge = CvBridge()


def main():
    # parse args
    parser = argparse.ArgumentParser(description="Convert video into a rosbag.")


