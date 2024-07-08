#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String, Float32MultiArray
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv
import numpy as np
import collections
import time
from firsttry.msg import ObjectWorldCoordinates_RobotID  # 替换为你的包名
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

class ImageConverter:
    def __init__(self):
        """Initialize the ImageConverter class, setting up ROS subscribers and internal variables."""
        self.bridge = CvBridge()
        self.rgb_sub = None
        self.depth_sub = None
        self.detect_sub = rospy.Subscriber("/tb3_3/detect_status", String, self.detect_status_callback)

        self.rgb_image = None
        self.depth_image = None
        self.mask = None
        self.rect_center = None
        self.rect_radius = None
        self.depth_buffer = collections.deque(maxlen=30)
        self.center_buffer = collections.deque(maxlen=30)
        self.z_average = None
        self.center_average = None
        self.start_time = None
        self.end_time = 3
        self.z_average_calculated = False
        self.center_average_calculated = False
        self.reset_done = False
        self.breakwhile = False
        self.box = None
        self.detecting = False  # Flag to start/stop detection
        self.robot_id = 1  # Default Robot_ID
        loginfo_color("Ready for start detect command!",Colors.GREEN)
    def rgb_callback(self, data):
        """Callback function for the RGB image subscriber."""
        if not self.detecting:
            return

        try:
            self.rgb_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"RGB Image conversion error: {e}")

    def depth_callback(self, data):
        """Callback function for the depth image subscriber."""
        if not self.detecting:
            return

        try:
            self.depth_image = self.bridge.imgmsg_to_cv2(data, "16UC1")
        except CvBridgeError as e:
            rospy.logerr(f"Depth Image conversion error: {e}")

    def detect_status_callback(self, data):
        # Expected format "start_detect:1"
        message_parts = data.data.split(':')
        if message_parts[0] == "start_detect":
            self.detecting = True
            self.breakwhile = False
            rospy.loginfo("Detection started.")
            self.subscribe_to_topics()
            
            # Extract Robot_ID if provided
            if len(message_parts) > 1 and message_parts[1].isdigit():
                self.robot_id = int(message_parts[1])
            else:
                self.robot_id = 1  # Default ID

            loginfo_color(f"Command received:{message_parts[0]},Robot ID = {message_parts[1]}",Colors.GREEN)


    def subscribe_to_topics(self):
        if self.rgb_sub is None:
            self.rgb_sub = rospy.Subscriber("/camera_tb3_3/color/image_raw", Image, self.rgb_callback)
        if self.depth_sub is None:
            self.depth_sub = rospy.Subscriber("/camera_tb3_3/aligned_depth_to_color/image_raw", Image, self.depth_callback)

    def unsubscribe_from_topics(self):
        if self.rgb_sub is not None:
            self.rgb_sub.unregister()
            self.rgb_sub = None
        if self.depth_sub is not None:
            self.depth_sub.unregister()
            self.depth_sub = None


    def process(self, image):
        """Process the RGB image to detect the largest blue object and draw relevant information."""
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        line = cv.getStructuringElement(cv.MORPH_RECT, (15, 15), (-1, -1))
        # mask = cv.inRange(hsv, (100, 43, 46), (124, 255, 255)) # Blue
        # Red
        mask1 = cv.inRange(hsv, (0, 120, 70), (10, 255, 255))
        mask2 = cv.inRange(hsv, (170, 120, 70), (180, 255, 255))
        mask = cv.bitwise_or(mask1,mask2)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, line)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        index = -1
        max_area = 0
        for c in range(len(contours)):
            area = cv.contourArea(contours[c])
            if area > max_area:
                max_area = area
                index = c

        if index >= 0:
            rect = cv.minAreaRect(contours[index])
            self.box = cv.boxPoints(rect)
            self.box = np.intp(self.box)
            self.mask = np.zeros_like(mask)
            cv.drawContours(self.mask, [self.box], 0, 255, -1)
            cv.drawContours(image, [self.box], 0, (255, 0, 0), 2)
            self.rect_center = (np.int32(rect[0][0]), np.int32(rect[0][1]))
            cv.circle(image, self.rect_center, 2, (0, 255, 0), 2, 8, 0)
            self.rect_radius = np.int32(min(rect[1][0], rect[1][1]) / 4)
            cv.putText(image, f"Center: {self.rect_center}", (self.rect_center[0] + 10, self.rect_center[1] + 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        else:
            self.rect_center = None
            self.rect_radius = None
            self.box = None

        return image

    def calculate_average_depth(self, depth_image, center, radius=30):
        """Calculate the average depth within a specified region, filtering outliers."""
        if center is not None and radius is not None:
            mask = np.zeros_like(depth_image, dtype=np.uint8)
            cv.circle(mask, center, radius, 255, -1)
            masked_depth = cv.bitwise_and(depth_image, depth_image, mask=mask)
            depth_values = masked_depth[mask != 0]
            depth_values = depth_values[depth_values != np.nan]
            if len(depth_values) == 0:
                return None

            median = np.median(depth_values)
            mad = np.median(np.abs(depth_values - median))
            threshold = 3 * mad
            filtered_depth_values = depth_values[np.abs(depth_values - median) < threshold]

            if len(filtered_depth_values) < 0.1 * len(depth_values):
                filtered_depth_values = depth_values

            if len(filtered_depth_values) == 0:
                return None

            mean_depth = np.mean(filtered_depth_values)
            return mean_depth

        return None

    def calculate_center_average(self):
        """Calculate the average center coordinates."""
        if len(self.center_buffer) > 0:
            center_points = np.array(self.center_buffer)
            self.center_average = np.mean(center_points, axis=0).astype(int)
        else:
            self.center_average = None

    def process_depth_image(self, depth_image):
        """Apply median blur to denoise the depth image."""
        depth_image = cv.medianBlur(depth_image,5)
        depth_image = cv.GaussianBlur(depth_image,(5,5),0)
        depth_image = depth_image.astype(np.float32)
        depth_image[depth_image==0] = np.nan
        return depth_image

    def calculate_z_average(self):
        """Calculate the average depth from the depth buffer."""
        if len(self.depth_buffer) > 0:
            depth_buffer_without_nan = self.depth_buffer[self.depth_buffer != np.nan]
            self.z_average = np.mean(depth_buffer_without_nan)
        else:
            self.z_average = None

    def reset_timing(self):
        """Reset timing and buffers."""
        self.start_time = None
        self.depth_buffer.clear()
        self.z_average_calculated = False
        self.reset_done = True

    def display_images(self):
        """Process and display RGB and depth images, calculating and displaying average depth and center coordinates."""
        if not self.detecting:
            return False, None, None

        if self.rgb_image is not None:
            result = self.process(self.rgb_image)

            if self.depth_image is not None:
                processed_depth_image = self.process_depth_image(self.depth_image)
                stabilized_depth_image = processed_depth_image

                if stabilized_depth_image is not None:
                    mean_depth = self.calculate_average_depth(stabilized_depth_image, self.rect_center, radius=self.rect_radius)
                    if mean_depth is not None and self.rect_center is not None:
                        current_time = time.time()

                        if self.start_time is None:
                            self.start_time = current_time
                            self.reset_done = False
                            rospy.loginfo("Started tracking target.")

                        elapsed_time = current_time - self.start_time

                        if elapsed_time <= self.end_time:
                            self.depth_buffer.append(mean_depth)
                            self.center_buffer.append(self.rect_center)
                            rospy.loginfo(f"Buffering depth value: {mean_depth:.2f} mm")
                            rospy.loginfo(f"Buffering center point: {self.rect_center}")
                            rospy.loginfo(f"Elapsed time: {elapsed_time:.2f} seconds")

                        if elapsed_time > self.end_time and not (self.z_average_calculated and self.center_average_calculated):
                            rospy.loginfo("Calculating z_average and center_average...")
                            self.calculate_z_average()
                            self.calculate_center_average()
                            self.z_average_calculated = True
                            self.center_average_calculated = True
                            rospy.loginfo(f"z_average: {self.z_average:.2f} mm")
                            rospy.loginfo(f"center_point: {self.center_average}")
                            self.breakwhile = True

                        # cv.putText(result, f"Avg Depth: {mean_depth:.2f} mm", (self.rect_center[0] + 10, self.rect_center[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv.putText(result, f"Avg Depth:", (self.rect_center[0] + 10, self.rect_center[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv.putText(result, f"{mean_depth:.2f} mm", (self.rect_center[0] + 10, self.rect_center[1] + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv.putText(result, f"Center: {self.rect_center}", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv.circle(result, self.rect_center, self.rect_radius, (0, 255, 255), 2)
                        rospy.loginfo(f"Average depth in the circular region: {mean_depth} mm at {elapsed_time:.2f} seconds")

                    depth_display = cv.normalize(stabilized_depth_image, None, 0, 255, cv.NORM_MINMAX)
                    depth_display = cv.convertScaleAbs(depth_display)
                    depth_display = cv.applyColorMap(depth_display, cv.COLORMAP_JET)

                    if self.rect_center is not None and self.rect_radius is not None:
                        if self.box is not None:
                            cv.drawContours(depth_display, [self.box], 0, (0, 0, 255), 2)
                        cv.circle(depth_display, self.rect_center, self.rect_radius, (0, 255, 255), 2)
                        cv.putText(depth_display, f"Avg Depth: {mean_depth:.2f} mm", (self.rect_center[0] - 10, self.rect_center[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv.putText(depth_display, f"Center: {self.rect_center}", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv.imshow("Depth Image", depth_display)

                if self.rect_center is None and not self.reset_done:
                    rospy.loginfo("No target detected. Resetting timing.")
                    self.reset_timing()

            cv.imshow("RGB Image", result)

        cv.waitKey(1)
        return self.breakwhile, self.z_average, self.center_average

def pixel_to_camera_with_z(point=[[0.0, 0.0]], z=1, distCoeffs=None):
    """Convert pixel coordinates to camera coordinates."""
    # 1280*720
    # K = np.array([[896.609803, 0.000000, 639.866297],
    #               [0.000000, 897.545099, 365.452675],
    #               [0.000000, 0.000000, 1.000000]], dtype=np.float32)
    # 640*480
    # K = np.array([[616.693237, 0.000000, 361.229892],
    #             [0.000000, 629.426514, 240.869800],
    #             [0.000000, 0.000000, 1.000000]], dtype=np.float32)
    # 424*240
    K = np.array([[302.914215087891, 0.000000, 210.587646484375],
                  [0.000000, 302.715454101562, 120.544738769531],
                  [0.000000, 0.000000, 1.000000]], dtype=np.float32)
    point = np.array(point, dtype=np.float32)
    MK = np.array(K, dtype=np.float32)
    if distCoeffs is None:
        distCoeffs = np.zeros((4, 1))
    pts_uv = cv.undistortPoints(np.expand_dims(point, axis=1), MK, distCoeffs) * z
    x, y = pts_uv[0][0]
    return x, y, z

def camera_to_base(point_wrt_camera_with_z):
    # extrinsic matrix
    R = np.array([[0,  0, 1],
                  [-1, 0, 0],
                  [0, -1, 0]])
    T = np.array([[90], [40], [82]])
    transform_matrix = np.hstack((R, T))
    transform_matrix = np.vstack((transform_matrix, [0, 0, 0, 1]))

    point_camera_homogeneous = np.hstack((point_wrt_camera_with_z, [1]))
    point_world = np.dot(transform_matrix, point_camera_homogeneous)
    point_world_in_meters = point_world / 1000.0
    point_world_in_meters[2] = point_world_in_meters[2] + 0.06
    point_world_in_meters[0] = point_world_in_meters[0] + 0.02
    rospy.loginfo(f"The point in world coordinates (m): {point_world_in_meters[:3]}")
    return point_world_in_meters

def main():
    """Main function to initialize the ROS node, process images, and publish object coordinates."""
    rospy.init_node('image_converter', anonymous=True)
    ic = ImageConverter()
    rate = rospy.Rate(10)  # 10 Hz

    # pub = rospy.Publisher('/object_world_coordinates', Float32MultiArray, queue_size=10)
    pub = rospy.Publisher('tb3_3/object_world_coordinates', ObjectWorldCoordinates_RobotID, queue_size=10)

    while not rospy.is_shutdown():
        if ic.detecting:
            breakwhile, z, center = ic.display_images()

            if breakwhile:
                if center is not None and z is not None:
                    x, y, z = pixel_to_camera_with_z(center, z)
                    rospy.loginfo(f"The coordinate wrt normalized camera frame: [{x}, {y}, {z}]")
                    point_wrt_camera_with_z = np.array([x, y, z])
                    rospy.loginfo(f"The coordinate wrt camera frame with z: {point_wrt_camera_with_z}")
                    point_world_in_meters = camera_to_base(point_wrt_camera_with_z)

                    # world_coordinates_msg = Float32MultiArray()
                    # world_coordinates_msg.data = point_world_in_meters[:3].tolist()
                    # pub.publish(world_coordinates_msg)

                    # Create and publish the custom message
                    world_coordinates_msg = ObjectWorldCoordinates_RobotID()
                    world_coordinates_msg.robot_id = str(ic.robot_id)
                    world_coordinates_msg.coordinates = point_world_in_meters[:3].tolist()
                    pub.publish(world_coordinates_msg)

                # Reset for the next detection and unsubscribe from topics
                ic.detecting = False
                ic.breakwhile = False
                ic.reset_timing()
                ic.unsubscribe_from_topics()
                cv.destroyAllWindows()

        rate.sleep()  # Ensure the loop runs at the specified rate

if __name__ == "__main__":
    main()


