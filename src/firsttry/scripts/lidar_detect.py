#! /usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

def find_consecutive_values(data,target_index,num_consecutive,tolerance):
        num_ranges = len(data.ranges)
        
        def get_consecutive(index,n,direction):
            consecutive_values = []
            for i in range(n):
                idx = (index + direction * i) % num_ranges
                if abs(data.ranges[idx]-data.ranges[target_index]<tolerance):
                    consecutive_values.append((data.ranges[idx],idx)) # list (ranges_value,idx)
                else:
                    break
            return consecutive_values
        
        # 尝试从目标索引向前和向后查找连续的n个值（分别考虑最小值在连续序列中的最左，中间，最右的位置）

        consecutive_values_forward = get_consecutive(target_index,num_consecutive,1)

        if num_consecutive % 2 == 1:
            num_left_half = (num_consecutive // 2)+1
            num_right_half = (num_consecutive // 2)+1
            consecutive_values_left_half_inverse = get_consecutive(target_index,num_left_half,-1)
            consecutive_values_right_half = get_consecutive(target_index,num_right_half,1)
            consecutive_values_left_half = consecutive_values_left_half_inverse.reverse() # 反转左半部分
            # 合并两个列表并去重
            # 去掉重复的 target_index
            if consecutive_values_left_half and consecutive_values_right_half:
                if consecutive_values_left_half[-1][1] == consecutive_values_right_half[0][1]:
                    consecutive_values_left_half.pop()
            # 合并列表
            conticonsecutive_values_bothway = consecutive_values_left_half + consecutive_values_right_half
        else: # num_consecutive is odd
            num_left_half = (num_consecutive // 2)
            num_right_half = (num_consecutive // 2)+1
            consecutive_values_left_half_inverse = get_consecutive(target_index,num_left_half,-1)
            consecutive_values_right_half = get_consecutive(target_index,num_right_half,1)
            consecutive_values_left_half = consecutive_values_left_half_inverse.reverse() # 反转左半部分
            # 合并两个列表并去重
            # 去掉重复的 target_index
            if consecutive_values_left_half and consecutive_values_right_half:
                if consecutive_values_left_half[-1][1] == consecutive_values_right_half[0][1]:
                    consecutive_values_left_half.pop()
            # 合并列表
            conticonsecutive_values_bothway = consecutive_values_left_half + consecutive_values_right_half

        consecutive_values_backward = get_consecutive(target_index,num_consecutive,1)

        if len(consecutive_values_forward) == num_consecutive:
            return consecutive_values_forward
        elif len(conticonsecutive_values_bothway) == num_consecutive:
            return conticonsecutive_values_bothway
        else:
            return consecutive_values_backward

def callback(data):
    # 设置最小和最大范围
    min_range = 0.15  # 最小范围 15cm
    max_range = 0.3  # 最大范围 30cm
    tolerance = 0.01 # 容差 1cm
    num_consecutive = 5  # 连续值的数量
    # 筛选出在指定范围内的距离
    valid_ranges = [r for r in data.ranges if min_range <= r <= max_range]

    if valid_ranges:
        # 找到最小值及其对应的索引
        target_distance = min(valid_ranges)
        target_index = data.ranges.index(target_distance)
        # 获取对应的强度值
        target_intensity = data.intensities[target_index]
        # 找到最小值附近的连续值
        consecutive_values = find_consecutive_values(data,target_index,num_consecutive,tolerance)
        if num_consecutive % 2 == 1:
            median_value = consecutive_values[num_consecutive//2][0]
            median_index = consecutive_values[num_consecutive//2][1]
        else:
            median_value = (consecutive_values[(num_consecutive//2)-1][0]+consecutive_values[num_consecutive//2][0])/2
            median_index = (consecutive_values[(num_consecutive//2)-1][1]+consecutive_values[num_consecutive//2][1])/2


        # 计算对应的角度
        angle_min = data.angle_min
        angle_increment = data.angle_increment
        target_angle = angle_min + median_index * angle_increment
        
        # 计算物体的笛卡尔坐标
        x = median_value * np.cos(target_angle)
        y = median_value * np.sin(target_angle)
        z = 0

        rospy.loginfo("Minimum distance within {:.2f}-{:2f}cm: {:.2f} meters at angle: {:.2f} radians with intensity: {:.2f}".format(min_range,max_range,target_distance, target_angle, target_intensity))
    else:
        rospy.loginfo("No valid distances found within the specified range.")






def lidar_detect():
    rospy.init_node('lidar_min_distance_detector', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, callback)


    # 等待一条消息
    rospy.wait_for_message("/scan", LaserScan)

if __name__ == '__main__':
    lidar_detect()
