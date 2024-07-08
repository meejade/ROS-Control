 #!/usr/bin/env python3
from __future__ import print_function
import rospy
import sys
import os



current_path=os.path.dirname(os.path.abspath(__file__))
current_path=os.path.abspath(current_path)

parent_path=os.path.dirname(current_path)
sys.path.append(parent_path)

from srv import AddTwoInts,AddTwoIntsResponse



def handle_add_two_ints(req):
	print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
	return AddTwoIntsResponse(req.a + req.b)
	
def add_two_ints_server():
	rospy.init_node('add_two_ints_server')
	s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
	print("Ready to add two ints.")
	rospy.spin()
	
if __name__ == "__main__":
	add_two_ints_server()
