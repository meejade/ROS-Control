#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan

def callback_scan(data):
    print(data.range)

def listener():
    rospy.init_node("Lidar_listener",anonymous=True)
    rospy.Subscriber("tb3_3/scan", LaserScan, callback_scan)
    rospy.spin()
if "__name__" == '__main__':
    listener()