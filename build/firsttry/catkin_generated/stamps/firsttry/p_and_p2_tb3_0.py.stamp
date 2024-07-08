#!/usr/bin/env python3
import sys
import rospy
import moveit_commander
import tf
import numpy as np
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import Float32MultiArray,Float64,String
from firsttry.msg import ObjectWorldCoordinates_RobotID

# ANSI转义序列定义颜色
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'  # 用于重置颜色

def loginfo_color(message, color):
    """
    使用指定颜色输出日志信息
    """
    rospy.loginfo(color + message + Colors.ENDC)

class ArmGripperController:
    def move_to_initial_joint_angles(self):
        initial_joint_angles = [0.0, -1.0, 0.3, 0.7]
        current_joint_angles = self.arm_group.get_current_joint_values()
        
        if self._angles_are_close(current_joint_angles, initial_joint_angles):
            loginfo_color("Already at the initial place.(tb3_0)", Colors.GREEN)
        else:
            loginfo_color("Go to the initial place.(tb3_0)", Colors.GREEN)
            self.move_arm_to_joints(initial_joint_angles)
        self.move_gripper(0.01)  # Open gripper to default position

    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('arm_gripper_controller',anonymous=True)

        self.robot_id = None
        self.arm_group = moveit_commander.MoveGroupCommander(name="arm",robot_description="tb3_0/robot_description", ns="tb3_0")
        self.gripper_group = moveit_commander.MoveGroupCommander(name="gripper",robot_description="tb3_0/robot_description", ns="tb3_0")

        self.target_position = None  # Store the target position received from the callback
        self.start_action = False

        # Subscribe to the topic with the target coordinates
        # rospy.Subscriber('/object_world_coordinates', Float32MultiArray, self.coordinate_callback)
        rospy.Subscriber('/tb3_0/object_world_coordinates', ObjectWorldCoordinates_RobotID, self.coordinate_callback)
        # Listening to the place object command
        rospy.Subscriber('/tb3_0/place_object', String, self.place_object_callback)

        # Publish the status of the action
        self.action_status_publisher = rospy.Publisher('/tb3_0/action_status', String, queue_size=10)
        # Detect again if the target is not within the workspace
        self.start_detect_publisher = rospy.Publisher('/tb3_0/detect_status', String, queue_size=10)
        # Publish the status of placing
        self.place_status_publisher = rospy.Publisher('/tb3_0/place_status', String, queue_size=10)
        # Move to initial joint angles
        self.move_to_initial_joint_angles()

        initial_pose = self.get_current_pose()
        loginfo_color(f"Initial Arm Pose: {initial_pose}",Colors.GREEN)
    
    def rotation_matrix_to_quaternion(self,R):
        quaternion = tf.transformations.quaternion_from_matrix(np.vstack([np.hstack([R, [[0], [0], [0]]]), [0, 0, 0, 1]]))
        return Quaternion(*quaternion)

    def is_within_work_space(self, target_position):
        waypoints = []

        # 获取当前姿态
        current_pose = self.get_current_pose()

        # 设置目标位置
        target_pose = Pose()
        target_pose.position = Point(target_position.x, target_position.y, target_position.z)

        # 第一种情况：与当前方向一致
        target_pose.orientation = current_pose.orientation
        waypoints.append(target_pose)

        (plan, fraction) = self.arm_group.compute_cartesian_path(
                            waypoints,   # waypoints to follow
                            0.01,        # eef_step
                            0.0)         # jump_threshold
        
        if fraction == 1.0:
            return True

        # 第二种情况：夹爪朝向垂直向下
        waypoints.clear()  # 清除之前的路径点
        # 旋转矩阵 R 表示垂直向下的方向
        R = np.array([[0, 0, 1],
                      [0, 1, 0],
                      [-1, 0, 0]])
        target_pose.orientation = self.rotation_matrix_to_quaternion(R)
        waypoints.append(target_pose)

        (plan, fraction) = self.arm_group.compute_cartesian_path(
                            waypoints,   # waypoints to follow
                            0.01,        # eef_step
                            0.0)         # jump_threshold
        
        return fraction == 1.0


    def coordinate_callback(self, msg):
        # # Extract coordinates from the message
        # coordinates = msg.data

        # Extract coordinates from the custom message
        coordinates = msg.coordinates
        self.robot_id = msg.robot_id  # 提取robot_id
        if len(coordinates) == 3:
            self.target_position = Point(coordinates[0], coordinates[1], coordinates[2])
            loginfo_color(f"Received target position: {self.target_position}, RobotID: {self.robot_id}",Colors.GREEN)

            if self.is_within_work_space(self.target_position):
                self.start_action = True
            else:
                loginfo_color("Target position out of working range. Waiting for another target position", Colors.RED)
                self.start_detect_publisher.publish(f"start_detect:{self.robot_id}")
                self.start_action = False

    def place_object_callback(self, msg):
        # Extract the command and robot ID from the message
        message_parts = msg.data.split(':')
        if message_parts[0] == "place":
            print("111")
            try:
                robot_id = message_parts[1]
                if int(robot_id) == int(self.robot_id):
                    print("2222")
                    # Define the target joint angles from the image
                    target_joint_angles = [0, 0.82, 0, -0.82]
                    loginfo_color(f"Received place command for robot ID {robot_id}. Moving to specified joint angles.", Colors.GREEN)
                    self.move_arm_to_joints(target_joint_angles)
                    loginfo_color("Moved to specified joint angles successfully. Robot ID = {robot_id}", Colors.GREEN)
                    self.move_gripper(0.01)  # Open gripper to release
                    self.move_arm_to_joints([0.0, -1.0, 0.3, 0.7]) # move back to the init pose
                    loginfo_color("Place sequence completed, waiting for next command. Robot ID = {robot_id}", Colors.CYAN)
                    # 发送表示动作执行完成的话题消息
                    self.place_status_publisher.publish(f"Placement completed: {self.robot_id}")

            except (ValueError, IndexError):
                rospy.logwarn(f"Invalid place_object message received. Robot ID = {robot_id}")


    def get_current_pose(self):
        current_pose = self.arm_group.get_current_pose().pose
        return current_pose
    
    def _positions_are_close(self, position1, position2, tolerance=0.02):
        return(
            abs(position1.x - position2.x) < tolerance and
            abs(position1.y - position2.y) < tolerance and
            abs(position1.z - position2.z) < tolerance
        )
    
    def move_arm_to_position(self,target_position):
        target_position_reached = False

        self.arm_group.set_position_target([target_position.x, target_position.y, target_position.z])
        plan_position = self.arm_group.go(wait=True)
        print(plan_position)
        self.arm_group.stop()
        self.arm_group.clear_pose_targets()
        if plan_position:
            loginfo_color(f"Arm movement successful(position). Robot ID = {self.robot_id}",Colors.GREEN)
        else:
            loginfo_color(f"Arm movement failed(position). Robot ID = {self.robot_id}",Colors.YELLOW)
            current_pose = self.get_current_pose()
            if current_pose:
                rospy.logwarn(f"Target Arm Position: {target_position}. Robot ID = {self.robot_id}")
        
        while not target_position_reached:
            loginfo_color(f"Position not reached. Robot ID = {self.robot_id}",Colors.YELLOW)
            current_pose = self.get_current_pose()
            if current_pose:
                    target_position_reached = self._positions_are_close(current_pose.position, target_position)
            else:
                rospy.logwarn(f"Failed to get current pose during check. Robot ID = {self.robot_id}")
                break
            rospy.sleep(0.1)

    def _poses_are_close(self, pose1, pose2, tolerance=0.05):
        position1 = pose1.position
        position2 = pose2.position
        orientation1 = pose1.orientation
        orientation2 = pose2.orientation
        return (
            abs(position1.x - position2.x) < tolerance and
            abs(position1.y - position2.y) < tolerance and
            abs(position1.z - position2.z) < tolerance and
            abs(orientation1.w - orientation2.w) < tolerance
        )
    
    def move_arm_to_pose(self, target_pose):
        target_pose_reached = False

        self.arm_group.set_pose_target(target_pose)

        while True:
            plan_pose = self.arm_group.go(wait=True)
            
            if plan_pose:
                loginfo_color(f"Arm movement successful(pose). Robot ID = {self.robot_id}", Colors.GREEN)
                break
            else:
                loginfo_color(f"Arm movement failed(pose). Robot ID = {self.robot_id}. Retrying...", Colors.YELLOW)
                current_pose = self.get_current_pose()
                # if current_pose:
                #     loginfo_color(f"Current Arm Pose: {current_pose}. Robot ID = {self.robot_id}",Colors.MAGENTA)
                #     loginfo_color(f"Target Arm Pose: {target_pose}, Robot ID = {self.robot_id}",Colors.MAGENTA)
                # else:
                #     rospy.logwarn(f"Failed to get current pose during retry. Robot ID = {self.robot_id}")
                        
                rospy.sleep(1)  # Add a small delay before retrying

        loginfo_color(f"before while loop. Robot ID = {self.robot_id}",Colors.GREEN)
        while not target_pose_reached:
                current_pose = self.get_current_pose()
                if current_pose:
                    target_pose_reached = self._poses_are_close(current_pose, target_pose)
                #     loginfo_color(f"Current Arm Pose: {current_pose}. Robot ID = {self.robot_id}",Colors.MAGENTA)
                #     loginfo_color(f"Target Arm Pose: {target_pose}. Robot ID = {self.robot_id}",Colors.MAGENTA)
                    
                    
                else:
                    rospy.logwarn(f"Failed to get current pose during check. Robot ID = {self.robot_id}")
                    break
                rospy.sleep(0.1)
        loginfo_color(f"break the while loop. Robot ID = {self.robot_id}",Colors.GREEN)
        self.arm_group.stop()
        self.arm_group.clear_pose_targets()

    def _angles_are_close(self, current_angles, target_angles, tolerance=0.2):
        return all(abs(current - target) < tolerance for current, target in zip(current_angles, target_angles))

    def move_arm_to_joints(self, joint_angles):
        self.arm_group.set_joint_value_target(joint_angles)
        plan_joints = self.arm_group.go(wait=True)
        self.arm_group.stop()
        self.arm_group.clear_pose_targets()
        if plan_joints:
            loginfo_color(f"Moved to target joint angles successfully. Robot ID = {self.robot_id}", Colors.GREEN)
        else:
            loginfo_color(f"Failed to move to target joint angles. Robot ID = {self.robot_id}", Colors.RED)
            current_joint_values = self.arm_group.get_current_joint_values()
            # if current_joint_values:
                # rospy.logwarn(f"Current Joint Values: {current_joint_values}. Robot ID = {self.robot_id}")
                # rospy.logwarn(f"Target Joint Values: {joint_angles}. Robot ID = {self.robot_id}")
            
        while not self._angles_are_close(self.arm_group.get_current_joint_values(), joint_angles):
            print(self.arm_group.get_current_joint_values())
            print(joint_angles)
            rospy.sleep(0.1)

    def move_gripper(self,target_gripper_value):
        rospy.sleep(1)
        try:
            current_gripper_value = self.gripper_group.get_current_joint_values()
            rospy.loginfo(f"Current Gripper Joint Values: {current_gripper_value}. Robot ID = {self.robot_id}")
            rospy.loginfo(f"Setting Gripper Position to: {target_gripper_value}. Robot ID = {self.robot_id}")
            self.gripper_group.set_joint_value_target([target_gripper_value, 0])
            plan_gripper = self.gripper_group.go(wait=True)
            self.gripper_group.stop()
            if plan_gripper:
                loginfo_color(f"Gripper movement successful. Robot ID = {self.robot_id}",Colors.GREEN)
            else:
                loginfo_color(f"Gripper movement failed. Robot ID = {self.robot_id}. Retry once more.",Colors.BLUE)
                plan_gripper = self.gripper_group.go(wait=True)
        except moveit_commander.MoveItCommanderException as e:
            rospy.logerr(f"Failed to set gripper joint target: {e}")

    def grasp_object(self, target_position):
        self.move_arm_to_position(target_position)
        self.move_gripper(-0.01)  # Close gripper to grasp
    
    def release_object(self, target_position):
        self.move_arm_to_position(target_position)
        self.move_gripper(0.01)  # Open gripper to release

    def move_to_home_pose(self):
        home_pose = Pose()
        home_pose.position = Point(0.197, 0.0, 0.29)
        home_pose.orientation.w = 1.0

        self.move_arm_to_pose(home_pose)

    def move_to_home_joints(self):
        home_joint_angles = [0.0, -1.0, 0.3, 0.7]
        self.move_arm_to_joints(home_joint_angles)

    def take_actions(self):
        rate = rospy.Rate(10)  # 设置循环频率为10Hz
        while not rospy.is_shutdown():
            if self.start_action:
                if not self._positions_are_close(self.get_current_pose().position, self.target_position):
                    self.move_gripper(0.01)  # Open gripper to default position
                    self.grasp_object(self.target_position)
                    self.move_to_home_joints()
                    # self.move_to_home_pose()
                    # self.move_gripper(0.01)  # Open gripper to default position

                    loginfo_color(f"Action sequence completed, waiting for next command. Robot ID = {self.robot_id}", Colors.CYAN)
                    self.start_action = False  # 重置 start_action 标志
                    # 确保在每次动作序列完成后重新初始化目标位置
                    self.target_position = None
                    # 发送表示动作执行完成的话题消息
                    # self.action_status_publisher.publish("Action completed")
                    self.action_status_publisher.publish(f"Action completed: {self.robot_id}")

            rate.sleep()

    
if __name__ == '__main__':
    try:
        controller = ArmGripperController()
        controller.take_actions()  # 启动动作循环
    except rospy.ROSInterruptException:
        pass
    finally:
        moveit_commander.roscpp_shutdown()