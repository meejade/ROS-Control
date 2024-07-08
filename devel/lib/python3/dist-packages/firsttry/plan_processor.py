#!/usr/bin/env python3

import asyncio
import json
import os
import pickle
import sys
import threading
import time
import numpy
import websockets as websockets
import pandas as pd
import websockets.extensions
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
import rospy

buffer = []
plan_dict = {}
plan_ready = False
is_paused = False
is_terminated = False

class AGV_Schedule:
    visit_time: float
    visit_point: str
    waiting_time: float
    charging_time: float
    x: float
    y: float
    status: int
    # direction: float
    def __init__(self,v_time,v_point,w_time,c_time,x,y,status):
        self.visit_time = v_time
        self.visit_point = v_point
        self.waiting_time = w_time
        self.charging_time = c_time
        self.x = x
        self.y = y
        self.status = status

def coordinates_transfer(plan):
    coord_dict = {}
    coord_df = pd.read_csv("physical layout.csv")
    coord_df.set_index('Point', inplace=True)
    for point in coord_df.iterrows():
        # coord_dict[str(point[0])] = [point[1][0], point[1][1]]
        coord_dict[str(point[0])] = [point[1][0], point[1][1], point[1][2]]
        # s = point[1][2]
    for agv in plan:
        for agv_plan in plan[agv]:
            agv_plan.x = coord_dict[agv_plan.visit_point][0]
            agv_plan.y = coord_dict[agv_plan.visit_point][1]
            agv_plan.status = coord_dict[agv_plan.visit_point][2]
            # agv_plan.status = s
            print("s=",agv_plan.status)



def data_process(data):
    global is_terminated
    global is_paused
    if data == "Unity Connected":
        print("Connection Success")
        return
    elif data == "Terminate":
        is_terminated = True
    elif data == "Pause":
        is_paused = True
        is_terminated = False
        buffer.append("command_request")
    elif data == "wait":
        time.sleep(2)
        buffer.append("command_request")
    elif data == "success":
        buffer.append("command_request")
    else:
        if is_paused:
            print("bypass")
            is_paused = False
            time.sleep(2)
            buffer.append("command_request")
            return
        time.sleep(2)
        buffer.append("command_request")
        plans = str(json.loads(data)["data"])
        print(plans)
        plans_per_agv = plans.split("]")
        for agv in plans_per_agv:
            if agv == "}":
                break
            agv_split = agv.split("[")
            agv_name = agv_split[0].split("\"")[1]
            agv_plans = []
            plan_split_1st = agv_split[1].split("}")
            print(plan_split_1st)
            for agv_plan in plan_split_1st:
                if agv_plan == "":
                    break
                agv_plan = ","+agv_plan
                agv_plan = agv_plan.split("{")[1]
                attributes = agv_plan.split(",")
                schedule = AGV_Schedule(0,"",0,0,0,0,0)
                for attribute in attributes:
                    variable = attribute.split(":")
                    if variable[0] == "\"agv_energy\"":
                        continue
                    else:
                        if variable[0] == " \"charging_time\"":
                            schedule.charging_time = variable[1]
                        elif variable[0] == " \"visit_point\"":
                            schedule.visit_point = variable[1].split("\"")[1]
                        elif variable[0] == " \"visit_time\"":
                            schedule.visit_time = variable[1]
                        elif variable[0] == " \"waiting_time\"":
                            schedule.waiting_time = variable[1]
                agv_plans.append(schedule)
            plan_dict[agv_name] = agv_plans
        coordinates_transfer(plan_dict)
        global plan_ready
        plan_ready = True

def get_plan_ready():
    return plan_ready

async def client_behavior():
    buffer.append("ROS Connected")
    buffer.append("command_request")
    while True:
        if is_terminated:
            print("exit2")
            exit()
        try:
            async with websockets.connect('ws://192.168.0.3:8002/', ping_interval=200) as ws:
                for i in buffer:
                    await ws.send(i)
                    print(f"Sent message: {i}")
                    message = await ws.recv()
                    print(f"Received message: {message}")
                    data_process(message)
                buffer.clear()
                print("buffer done")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connect error: {e}")

    # while True:
    #     async with websockets.connect('ws://192.168.0.5:8002/', ping_interval=200) as ws:
    #         for i in buffer:
    #             await ws.send(i)
    #             print(f"Sent message: {i}")
    #             message = await ws.recv()
    #             print(f"Received message: {message}")
    #             data_process(message)
    #         buffer.clear()
    #         print("buffer done")

# if __name__ == "__main__":
#     asyncio.run(client_behavior())
