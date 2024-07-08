#!/usr/bin/env python3
from __future__ import print_function
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import sys, select, os
import rospy
import math

current_path=os.path.dirname(os.path.abspath(__file__))
current_path=os.path.abspath(current_path)

parent_path=os.path.dirname(current_path)
sys.path.append(parent_path)

from srv import chat,chatResponse
    
def odom_callback(msg):
	global current_position
	current_position = msg.pose.pose.position
	
def calculate_distance(position1,position2):
	distance = math.sqrt((position1.x-position2.x)**2+(position1.y-position2.y)**2)
	return distance

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
			run_duration = 10.0
			pub_duration = 0.5
			start_time = rospy.get_time()
		
			while (rospy.get_time() - start_time < run_duration):    
			
				# for tb3_0
				target_linear_vel_0  = 0.5
				twist0 = Twist()
				twist0.linear.x = target_linear_vel_0; twist0.linear.y = 0.0; twist0.linear.z = 0.0
				twist0.angular.x = 0.0; twist0.angular.y = 0.0; twist0.angular.z = 0.0
			
				# for tb3_1
				target_angular_vel_1  = 0.5
				twist1 = Twist()
				twist1.linear.x = 0.0; twist1.linear.y = 0.0; twist1.linear.z = 0.0
				twist1.angular.x = 0.0; twist1.angular.y = 0.0; twist1.angular.z = target_angular_vel_1
			

				pub.publish(twist0)
				pub_0.publish(twist1)
				rospy.sleep(pub_duration)		
			return chatResponse("Run!")
		else:
			print("Returning: Hold")
			return chatResponse("Hold")
			
			
	elif req.a == "Time":
	
		run_duration = 10.0
		pub_duration = 0.5
		start_time = rospy.get_time()
		
		while (rospy.get_time() - start_time < run_duration):    
			
			# for tb3_0
			target_linear_vel_0  = 0.5
			twist0 = Twist()
			twist0.linear.x = target_linear_vel_0; twist0.linear.y = 0.0; twist0.linear.z = 0.0
			twist0.angular.x = 0.0; twist0.angular.y = 0.0; twist0.angular.z = 0.0
			
			# for tb3_1
			target_angular_vel_1  = 0.5
			twist1 = Twist()
			twist1.linear.x = 0.0; twist1.linear.y = 0.0; twist1.linear.z = 0.0
			twist1.angular.x = 0.0; twist1.angular.y = 0.0; twist1.angular.z = target_angular_vel_1
			

			pub.publish(twist0)
			pub_0.publish(twist1)
			rospy.sleep(pub_duration)		
			
		print("Returning: Move Ready")
		return chatResponse("Move Ready")


	elif req.a == "Odom":
	
		target_distance = 1.0
		start_position = current_position
		pub_duration = 0.5
		
		while (calculate_distance(current_position,start_position) < target_distance):
			# for tb3_0
			target_linear_vel_0  = 0.05
			twist0 = Twist()
			twist0.linear.x = target_linear_vel_0; twist0.linear.y = 0.0; twist0.linear.z = 0.0
			twist0.angular.x = 0.0; twist0.angular.y = 0.0; twist0.angular.z = 0.0
			
			
			pub.publish(twist0)
			pub_0.publish(twist0)
			rospy.sleep(pub_duration)	
		
						
		print("Returning: Move Ready")
		return chatResponse("Move Ready")
		
		
	elif req.a == "Stop":
		twist_stop = Twist()
		twist_stop.linear.x = 0.0; twist_stop.linear.y = 0.0; twist_stop.linear.z = 0.0
		twist_stop.angular.x = 0.0; twist_stop.angular.y = 0.0; twist_stop.angular.z = 0.0
		
		pub.publish(twist_stop)
		pub_0.publish(twist_stop)
		print("Returning: Ready to stop")
		return chatResponse("Ready to stop")
		
		
	else:
		print("Returning: Wrong Command")
		return chatResponse("Error!")
		
	
def chat_server():
	rospy.init_node('chat_server')
	s = rospy.Service('chat', chat, handle_chat)
	print("Ready.")
	rospy.spin()
	
	
if __name__ == "__main__":
	rospy.Subscriber('tb3_0/odom',Odometry,odom_callback)
	global num
	num = 0
	global pub
	pub = rospy.Publisher('tb3_0/cmd_vel', Twist, queue_size=10)
	global pub_0
	pub_0 = rospy.Publisher('tb3_1/cmd_vel', Twist, queue_size=10)
	chat_server()
