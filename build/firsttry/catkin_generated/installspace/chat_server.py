#!/usr/bin/env python3
from __future__ import print_function
import rospy
import sys
import os



current_path=os.path.dirname(os.path.abspath(__file__))
current_path=os.path.abspath(current_path)

parent_path=os.path.dirname(current_path)
sys.path.append(parent_path)

from srv import chat,chatResponse


def handle_chat(req):
	if req.a == "Data":
		print("Returning: plan")
		return chatResponse("plan")
	elif req.a == "Ready?":
		global num
		num = num + 1
		print("Returning: Wait")
		return chatResponse("Wait")
	elif req.a == "Execution":
		if num == 2:
			print("Returning: Run!")
			return chatResponse("Run!")
		else:
			print("Returning: Hold")
			return chatResponse("Hold")
	else:
		print("Returning: Wrong Command")
		return chatResponse("Error!")
	
def chat_server():
	rospy.init_node('chat_server')
	s = rospy.Service('chat', chat, handle_chat)
	print("Ready.")
	rospy.spin()
	
if __name__ == "__main__":
	global num
	num = 0
	chat_server()
