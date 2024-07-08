#!/usr/bin/env python3
from __future__ import print_function
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped, PoseStamped
from nav_msgs.msg import Odometry
import tf
import sys, select, os
import rospy
import math
import asyncio
import threading
import numpy
import json
import std_msgs
from std_msgs.msg import String
import tf.transformations

current_path=os.path.dirname(os.path.abspath(__file__))
current_path=os.path.abspath(current_path)

parent_path=os.path.dirname(current_path)
sys.path.append(parent_path)

import plan_processor
from srv import chat,chatResponse

name_dict = {}
current_position = {}
current_orientation = {}
angular_speed = 0.1
linear_speed = 0.2
rotation_period = 4
speed = 0.14
pick_order = {}
place_order = {}
def get_key_by_value(dict, value):
	for k,v in dict.items():
		if v==value:
			return k
	print("name not found")
    
def poseAMCLCallback(msg, name):
	print(name)	
	current_position[name] = msg.pose.pose.position
	current_orientation[name] = msg.pose.pose.orientation
	if plan_processor.get_plan_ready():
		agv_name = get_key_by_value(name_dict,name)
		plan_processor.buffer.append(json.dumps({"command": "trace:"+agv_name, "data": 
																		   [current_position[name].x,current_position[name].y]}))

def detect_status_callback(msg, name):
	temp = msg.data
	temp = temp.split(":")[0]
	if temp == "Action completed":
		pick_order[name] = True
	else:
		pick_order[name] = False

def place_status_callback(msg, name):
	temp = msg.data
	temp = temp.split(":")[0]
	if temp == "Placement completed":
		pick_order[name] = True
	else:
		pick_order[name] = False

def acos(x):
	y = numpy.arccos(x)
	y = round(y, 2)
	return [y,round((-1*y),2)]

def asin(x):
	y = numpy.arcsin(x)
	z = float(3.1415926-y)
	return [round(y,2),round(z,2)]

def spec_asin(x):
	y = numpy.arccos(x)
	y =y*2
	z = float(3.1415926-y)
	return [round(y,2),round(z,2)]

def cos_twice(cos, sin):
	return (cos**2-sin**2)

def sin_twice(cos, sin):
	return (2*cos*sin)

def calculate_target_orientation_new(position1, position2, c):
	delta_x = position2.x-position1.x
	cos_theta = delta_x/c
	delta_y = position2.y-position1.y
	sin_theta = delta_y/c
	return [cos_theta,sin_theta]

def intersec(list1,list2):
	for i in list1:
		for j in list2:
			if abs(i-j)<=0.02:
				return i
	
def calculate_distance(position1,position2):
	distance = math.sqrt((position1.x-position2.x)**2+(position1.y-position2.y)**2)
	return distance

def calculate_target_orientation(position1, position2, c):
	delta_x = position2.x-position1.x
	cos_theta = delta_x/c
	delta_y = position2.y-position1.y
	sin_theta = delta_y/c
	angular = numpy.arctan2(sin_theta,cos_theta)
	return angular

def calculate_pose_orientaiton(orientation):
	quaternion = [orientation.x, orientation.y, orientation.z, orientation.w]
	triplet = tf.transformations.euler_from_quaternion(quaternion)
	return triplet[2]

def alternate_translate(namespace:str, target, distance):
	global cmd_pub_dict
	twist0 = Twist()
	twist0.linear.x = linear_speed
	twist0.linear.y = 0
	twist0.linear.z = 0
	twist0.angular.x = 0
	twist0.angular.y = 0
	twist0.angular.z = 0
	while calculate_distance(current_position[namespace],target) > 0.05:
		cmd_pub_dict[namespace].publish(twist0)
	print("arrived")
	return float(distance/linear_speed)
		
def alternate_rotate(namespace:str, origin, target, distance):
	ang_origin = calculate_pose_orientaiton(current_orientation[namespace])
	ang_target = calculate_target_orientation(origin, target, distance)
	quaternion_target = tf.transformations.quaternion_from_euler(0, 0, ang_target)
	delta_ang = ang_target - ang_origin
	print("ori: ",ang_origin,", tar: ",ang_target, ", delta: ",delta_ang)
	angular_vel = 0
	if delta_ang > 0:
		angular_vel = angular_speed
	else:
		angular_vel = angular_speed * (-1)
	twist0 = Twist()
	twist0.linear.x = 0
	twist0.linear.y = 0
	twist0.linear.z = 0
	twist0.angular.x = 0
	twist0.angular.y = 0
	twist0.angular.z = angular_vel
	while abs(ang_target-tf.transformations.euler_from_quaternion([current_orientation[namespace].x, current_orientation[namespace].y,
															    current_orientation[namespace].z, current_orientation[namespace].w])[2]) > 0.018:
		print(tf.transformations.euler_from_quaternion([current_orientation[namespace].x, current_orientation[namespace].y,
															    current_orientation[namespace].z, current_orientation[namespace].w])[2])
		cmd_pub_dict[namespace].publish(twist0)
		rospy.sleep(0.5)
	return float(delta_ang/angular_speed)


def move_to_start(namespace:str, start_point):
	distance = calculate_distance(current_position[namespace],start_point)
	angular = calculate_target_orientation(current_position[namespace], start_point, distance)
	# angular2 = calculate_pose_orientaiton(current_orientation[namespace])
	# angular = angular1 - angular2
	print("d=",distance,",a=",angular)
	time_translate = float(distance/speed)
	print("time: ", time_translate)
	rospy.sleep(float(start_point.waiting_time) + float(start_point.charging_time)-time_translate -3)
	goal = PoseStamped()
	goal.header.frame_id = "map"
	goal.header.stamp = rospy.Time.now()
	#move to start
	goal.pose.position.x = start_point.x
	goal.pose.position.y = start_point.y
	quaternion = tf.transformations.quaternion_from_euler(0,0,angular)
	goal.pose.orientation.x = quaternion[0]
	goal.pose.orientation.y = quaternion[1]
	goal.pose.orientation.z = quaternion[2]
	goal.pose.orientation.w = quaternion[3]

	pub_dict[namespace].publish(goal)

	#rotate_time = alternate_rotate(namespace, current_position[namespace], start_point, distance)
	rospy.sleep(time_translate+3)

	print("Done move to Start")
	#rospy.sleep(float(start_point.waiting_time) + float(start_point.charging_time)-time_translate)
	#translate
	# goal = PoseStamped()
	# goal.header.frame_id = "map"
	# goal.header.stamp = rospy.Time.now()
	# goal.pose.position.x = start_point.x
	# goal.pose.position.y = start_point.y
	# goal.pose.orientation.x = quaternion[0]
	# goal.pose.orientation.y = quaternion[1]
	# goal.pose.orientation.z = quaternion[2]
	# goal.pose.orientation.w = quaternion[3]
	# pub_dict[namespace].publish(goal)
	# rospy.sleep(time_translate + 30)
	#translate_time = alternate_translate(namespace, start_point, distance)
	#rospy.sleep(60-rotate_time-translate_time)
	# print("Done translate to Start")




def move_to(namespace:str, origin, target):
	distance = calculate_distance(origin,target)
	angular = calculate_target_orientation(origin, target, distance)
	#- calculate_pose_orientaiton(current_orientation[namespace])
	print("d=",distance,",a=",angular)
	goal = PoseStamped()
	goal.header.frame_id = "map"
	goal.header.stamp = rospy.Time.now()
	#rotate
	goal.pose.position.x = origin.x
	goal.pose.position.y = origin.y
	quaternion = tf.transformations.quaternion_from_euler(0,0,angular)
	goal.pose.orientation.x = quaternion[0]
	goal.pose.orientation.y = quaternion[1]
	goal.pose.orientation.z = quaternion[2]
	goal.pose.orientation.w = quaternion[3]

	pub_dict[namespace].publish(goal)
	rospy.sleep(rotation_period)
	print("Done rotate")
	#translate
	goal.pose.position.x = target.x
	goal.pose.position.y = target.y

	pub_dict[namespace].publish(goal)
	#alternate_translate(namespace, target, distance)
	translate_time = float(distance/speed)
	print("time: ", translate_time)
	rospy.sleep(float(target.waiting_time) + float(target.charging_time)+translate_time+1)
	print("Done translate")


	



def stop_robot():
	twist0 = Twist()
	twist0.linear.x = 0.0
	twist0.linear.y = 0.0
	twist0.linear.z = 0.0
	twist0.angular.x = 0.0
	twist0.angular.y = 0.0
	twist0.angular.z = 0.0
	for i in pub_dict:
		i.publish(twist0)
	print("STOP")
	return

def handle_chat(req):

	if req.a == "connect":
		global num
		num = num+1
		print ("Connected!")
		return chatResponse(list(plan_processor.plan_dict.keys())[num-1])
		
	else:
		print(req.a)
		names = str(req.a).split(":")
		if len(names) != 2:
			return chatResponse("Error!")
		else:
			if names[0]=="request plan":
				chatResponse("finish running")
				print(names[1],": request plan")
				if plan_processor.get_plan_ready() and num == num_agv and len(name_dict.keys()) == num_agv:
					# global trigger
					# trigger += 1
					
					agv_name = list(name_dict.keys())[list(name_dict.values()).index(names[1])]
					for i in plan_processor.plan_dict[agv_name]:
						print("is_pause: ",plan_processor.is_paused,", is_terminate: ",plan_processor.is_terminated)
						while plan_processor.is_paused:
							print("paused and waiting.")
							rospy.sleep(2)
							plan_processor.buffer.append("command_request")
						if plan_processor.is_terminated:
							print("exit1")
							exit()
						else:
							print(i.visit_point, i.x, i.y)
							if plan_processor.plan_dict[agv_name].index(i) == 0:
								move_to_start(names[1],i)
								plan_processor.buffer.append(json.dumps({"command": "run", "data": ""}))
								#move_to(names[1], current_position[names[1]], i)
							else:
								j = plan_processor.plan_dict[agv_name].index(i)
								#move_to(names[1], current_position[names[1]], i)
								# print(i.x, i.y)
								move_to(names[1], plan_processor.plan_dict[agv_name][j-1], i)
					return chatResponse("finish running")
				else:
					return chatResponse("wait for plan")				
			else:
				name_dict[names[0]] = names[1]
				print("start!!!!!!!!!!!!!")
				global pub_dict
				global sub_list
				topic_name = names[1]+'/move_base_simple/goal'
				pub = rospy.Publisher(topic_name, PoseStamped, queue_size = 10)
				pub_dict[names[1]] = pub
				topic_name = names[1]+'/cmd_vel'
				cmd_pub = rospy.Publisher(topic_name, Twist, queue_size = 10)
				cmd_pub_dict[names[1]] = cmd_pub
				topic_name = names[1]+'/amcl_pose'
				sub = rospy.Subscriber(topic_name, PoseWithCovarianceStamped, poseAMCLCallback, callback_args=names[1])
		#		sub = rospy.Subscriber(topic_name, Odometry, odom_callback, callback_args='tb3_'+str(i))
				sub_list.append(sub)
				return chatResponse("connected")
		

# async def position_sender():
# 	pos_sub = rospy.Subscriber('tb3_3/amcl_pose', PoseWithCovarianceStamped, poseAMCLCallback, callback_args='tb3_3')
# 	print(current_position.keys())
# 	agv_name = "Y_V01"
# 	while True:
# 		x = current_position['tb3_3'].x
# 		y = current_position['tb3_3'].y
# 		plan_processor.buffer.append(json.dumps({"command": "trace:"+agv_name, "data": [x,y]}))
# 		rospy.sleep(1)

async def chat_server():
	rospy.init_node('chat_server')
	s = rospy.Service('chat', chat, handle_chat)
	print("Ready.")

	await asyncio.Future()
	
async def start():
	task1 = asyncio.create_task(chat_server())
	task2 = asyncio.create_task(plan_processor.client_behavior())
	#task3 = asyncio.create_task(position_sender())
	await asyncio.gather(task1, task2)

class pos():
	x:float
	y:float
	def __init__(self, x:float, y:float):
		self.x = x
		self.y = y
	
class test_orient:
	x:float
	y:float
	z:float
	w:float
	def __init__(self, w,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		self.w = w

if __name__ == "__main__":
	rospy.init_node('arm_gripper_controller')




	# global num_agv
	# num_agv = int(sys.argv[1])
	# print(num_agv)
	# global num
	# num = 0
	# global pub_dict
	# global sub_list
	# global cmd_pub_dict
	# pub_dict = {}
	# cmd_pub_dict = {}
	# sub_list = []





	# s = rospy.Subscriber('tb3_3/amcl_pose', PoseWithCovarianceStamped, poseAMCLCallback, callback_args='tb3_3')
	p1_pick = rospy.Publisher('/tb3_0/detect_status', String, queue_size=10)
	p2_pick = rospy.Publisher('/tb3_3/detect_status', String, queue_size=10)
	p1_place = rospy.Publisher('/tb3_0/place_object', String, queue_size=10)
	p2_place = rospy.Publisher('/tb3_3/place_object', String, queue_size=10)
	p1_sub_pick = rospy.Subscriber('/tb3_0/detect_status',String, detect_status_callback, callback_args='tb3_0')
	p2_sub_pick = rospy.Subscriber('/tb3_3/detect_status',String, detect_status_callback, callback_args='tb3_0')
	p1_sub_place = rospy.Subscriber('/tb3_0/place_status',String, place_status_callback, callback_args='tb3_0')
	p2_sub_place = rospy.Subscriber('/tb3_3/place_status',String, place_status_callback, callback_args='tb3_0')
	rospy.sleep(1)
	print(p1_pick)
	print(p2_pick)
	picker = String()
	picker.data = "start_detect:3"
	p2_pick.publish(picker)
	print(picker.data)
	picker.data = 'start_detect:0'
	p1_pick.publish("start_detect:0")
	print(picker.data)
	rospy.sleep(40)
	p1_place.publish("place:0")
	p2_place.publish("place:3")
	print("jjjjjjjjjjj")
	rospy.spin()

	# asyncio.run(start())
