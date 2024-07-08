 #!/usr/bin/env python3

from __future__ import print_function

import sys
import rospy
import os

current_path=os.path.dirname(os.path.abspath(__file__))
current_path=os.path.abspath(current_path)

parent_path=os.path.dirname(current_path)
sys.path.append(parent_path)

from srv import *
 
def chat_client(x):
    rospy.wait_for_service('chat')
    sleep_duration = rospy.Duration(2.0)
    try:
        chats = rospy.ServiceProxy('chat', chat)
        resp1 = chats(x)
        print("%s"%resp1.b)
        if (resp1.b == "plan"):
        	chat_client("Ready?")
        elif (resp1.b == "Wait"):
        	chat_client("Execution")
        elif (resp1.b == "Hold"):
        	rospy.sleep(sleep_duration)
        	chat_client("Execution")
        elif (resp1.b == "Run!"):
        	print("Success!")
        return resp1.b
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x]"%sys.argv[0]

if __name__ == "__main__":
	if len(sys.argv) == 2:
		x = str(sys.argv[1])
	else:
		print(usage())
		sys.exit(1)
	print("Requesting %s"%x)
	chat_client(x)
