#! /usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
from firsttry.msg import ObjectWorldCoordinates_RobotID
class Lidar_detector:
    def __init__(self,namespace):
        self.lidar_scan_sub = rospy.Subscriber(namespace+"/scan", LaserScan, self.callback)
        self.x = None
        self.y = None
        self.z = None
        self.name = namespace

    def get_consecutive(self,target_index,n,direction,valid_ranges,num_valid_ranges,tolerance,target_index_in_valid,num_ranges):
        consecutive_values = []
        for i in range(n):
            idx = (target_index_in_valid + direction * i) % num_valid_ranges
            index = (target_index + direction * i) % num_ranges
            if abs(valid_ranges[idx]-valid_ranges[target_index_in_valid]<tolerance):
                consecutive_values.append((valid_ranges[idx],index)) # list (ranges_value,index)
            else:
                break
            print(f"direction:{direction},consecutive_values:{consecutive_values}")
        return consecutive_values
    
    def find_consecutive_values(self,data,target_index,num_consecutive,tolerance,valid_ranges,num_valid_ranges,target_index_in_valid):
            num_ranges = len(data.ranges)
            # 尝试从目标索引向前和向后查找连续的n个值（分别考虑最小值在连续序列中的最左，中间，最右的位置）

            consecutive_values_forward = self.get_consecutive(target_index,num_consecutive,1,valid_ranges,num_valid_ranges,tolerance,target_index_in_valid,num_ranges)
            if len(consecutive_values_forward) == num_consecutive:
                return consecutive_values_forward
            else:
                if num_consecutive % 2 == 1:
                    num_left_half = (num_consecutive // 2)+1
                    num_right_half = (num_consecutive // 2)+1
                    consecutive_values_left_half_inverse = self.get_consecutive(target_index,num_left_half,-1,num_ranges,tolerance,target_index,data)
                    print(f"reverse:{consecutive_values_left_half_inverse}")
                    consecutive_values_right_half = self.get_consecutive(target_index,num_right_half,1,num_ranges,tolerance,target_index,data)
                    consecutive_values_left_half = consecutive_values_left_half_inverse.reverse() # 反转左半部分
                    print(f"xleft_half:{consecutive_values_left_half}")
                    print(f"xright_half:{consecutive_values_right_half}")
                    # 合并两个列表并去重
                    # 去掉重复的 target_index
                    if consecutive_values_left_half and consecutive_values_right_half:
                        if consecutive_values_left_half[-1][1] == consecutive_values_right_half[0][1]:
                            consecutive_values_left_half.pop()
                    # 合并列表
                    conticonsecutive_values_bothway = consecutive_values_left_half + consecutive_values_right_half
                else: # num_consecutive is even
                    num_left_half = (num_consecutive // 2)
                    num_right_half = (num_consecutive // 2)+1
                    consecutive_values_left_half = self.get_consecutive(target_index,num_left_half,-1,num_ranges,tolerance,target_index,data)
                    consecutive_values_right_half = self.get_consecutive(target_index,num_right_half,1,num_ranges,tolerance,target_index,data)
                    consecutive_values_left_half.reverse() # 反转左半部分
                    print(f"left_half:{consecutive_values_left_half}")
                    print(f"right_half:{consecutive_values_right_half}")
                    # 合并两个列表并去重
                    # 去掉重复的 target_index
                    if consecutive_values_left_half and consecutive_values_right_half:
                        if consecutive_values_left_half[-1][1] == consecutive_values_right_half[0][1]:
                            consecutive_values_left_half.pop()
                    # 合并列表
                    conticonsecutive_values_bothway = consecutive_values_left_half + consecutive_values_right_half
                if len(conticonsecutive_values_bothway) == num_consecutive:
                    return conticonsecutive_values_bothway
                else:
                    consecutive_values_backward = self.get_consecutive(target_index,num_consecutive,-1,num_ranges,tolerance,target_index,data)
                    if len(consecutive_values_backward) == num_consecutive:
                        return consecutive_values_backward
                    else:
                        rospy.logerr("No range values in a row meet the requirement!")

    def callback(self,data):
        # 设置最小和最大范围
        min_range = 0.15  # 最小范围 15cm
        max_range = 0.3 # 最大范围 30cm
        tolerance = 0.02 # 容差 5cm
        num_consecutive = 15  # 连续值的数量

        num_range = len(data.ranges)
        print(f"Total num of ranges:{num_range}")

        # 筛选出在指定范围内的距离
        valid_ranges = [r for r in data.ranges if min_range <= r <= max_range]
        # Find indices of valid ranges
        valid_indices = [i for i, r in enumerate(data.ranges) if min_range <= r <= max_range]
        num_valid_ranges = len(valid_ranges)
        print("Valid Ranges:", valid_ranges)
        print("Indices of Valid Ranges:", valid_indices)

        if valid_ranges:
            # 找到最小值及其对应的索引
            target_distance = min(valid_ranges)
            target_index = data.ranges.index(target_distance)
            target_index_in_valid = valid_ranges.index(target_distance)
            print(f"target_index:{target_index}")
            # 获取对应的强度值
            target_intensity = data.intensities[target_index]
            # 找到最小值附近的连续值
            consecutive_values = self.find_consecutive_values(data,target_index,num_consecutive,tolerance,valid_ranges,num_valid_ranges,target_index_in_valid)
            print(consecutive_values)
            if num_consecutive % 2 == 1:
                middle_value = consecutive_values[num_consecutive//2][0]
                middle_index = consecutive_values[num_consecutive//2][1]
            else:
                middle_value = (consecutive_values[(num_consecutive//2)-1][0]+consecutive_values[num_consecutive//2][0])/2
                middle_index = consecutive_values[(num_consecutive//2)-1][1]+0.5
            print("------------------------")
            print(middle_value)
            print(middle_index)
            print("---------------------------")
            # 计算对应的角度
            angle_min = data.angle_min
            angle_increment = data.angle_increment
            target_angle = angle_min + middle_index * angle_increment
            
            # 计算物体的笛卡尔坐标
            self.x = middle_value * np.cos(target_angle)
            self.y = middle_value * np.sin(target_angle)
            self.z = 0.16
            print(f"world coordinate: [{self.x},{self.y},{self.z}]")
            rospy.loginfo("Minimum distance within {:.2f}-{:2f}cm: {:.2f} meters at angle: {:.2f} radians with intensity: {:.2f}".format(min_range,max_range,target_distance, target_angle, target_intensity))
        else:
            rospy.loginfo("No valid distances found within the specified range.")

    def lidar_detect(self):
        #rospy.init_node('lidar_min_distance_detector', anonymous=True)
        
        pub = rospy.Publisher(self.name+'/object_world_coordinates', ObjectWorldCoordinates_RobotID, queue_size=10)

        # 等待一条消息
        rospy.wait_for_message(self.name+"/scan", LaserScan)

        world_coordinate_msg = ObjectWorldCoordinates_RobotID()
        world_coordinate_msg.robot_id = str(3)
        world_coordinate_msg.coordinates = [self.x,self.y,self.z]
        print(self.x,",",self.y,",",self.z)
        pub.publish(world_coordinate_msg)

if __name__ == '__main__':
    Ld = Lidar_detector("tb3_3")
    Ld.lidar_detect()
    # rospy.spin()
