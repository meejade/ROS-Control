#!/usr/bin/env python3 
 
import asyncio  
import json  
import websockets  
import rospy  
from nav_msgs.msg import Odometry  
 
async def ros_publisher(websocket, path):  
    while True: 
        rospy.sleep(0.5)
        data = await queue.get()  
        await websocket.send(data)  
        response = await websocket.recv()  
        print(f"From client: {response}") 
 
# ROS subscriber callback for the odom topic 
def callback(data):  
    x = data.pose.pose.position.x  
    y = data.pose.pose.position.y  
    asyncio.run_coroutine_threadsafe(queue.put(json.dumps({'x': x, 'y': y})), loop) 
 
if __name__ == "__main__": 
    rospy.init_node('turtlebot_websocket_server') 
    rospy.Subscriber("odom", Odometry, callback) 
 
    queue = asyncio.Queue()  
    loop = asyncio.get_event_loop()  
 
    # Make sure the IP address and port are correctly configured for your network environment 
    start_server = websockets.serve(ros_publisher, '192.168.0.3', 9876) 
    loop.run_until_complete(start_server)  
    loop.run_forever() 
