 #!/usr/bin/env python3

from __future__ import print_function

import sys
import rospy
import os
from geometry_msgs.msg import Twist

current_path=os.path.dirname(os.path.abspath(__file__))
current_path=os.path.abspath(current_path)

parent_path=os.path.dirname(current_path)
sys.path.append(parent_path)

from srv import *

def callback(data):
    print(data)

def chat_client(x):
    rospy.wait_for_service('chat')
    sleep_duration = rospy.Duration(2.0)
    try:
        chats = rospy.ServiceProxy('chat', chat)
        resp1 = chats(x)
        print("%s"%resp1.b)
        if (resp1.b == "connected"):
            chat_client("request plan")
        elif (resp1.b == "wait for plan"):
            rospy.sleep(sleep_duration)
            chat_client("request plan")
        elif (resp1.b == "plan ready"):
            chat_client("ready to run")        	
        return resp1
        
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x]"%sys.argv[0]

if __name__ == "__main__":
	rospy.init_node('mover_2')
	rospy.Subscriber('tb3_1/cmd_vel',Twist,callback)
	if len(sys.argv) == 2:
		x = str(sys.argv[1])
	else:
		print(usage())
		sys.exit(1)
	print("Requesting %s"%x)
	chat_client(x)
	rospy.spin()
