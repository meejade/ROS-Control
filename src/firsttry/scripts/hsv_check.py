# # For web camera
# import cv2
# import os
# cap = cv2.VideoCapture(0)
# while True:
#     # Get a frame
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Show a frame
#     cv2.imshow("capture", frame)

#     # Press 'q' to save the image and exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         # Expand the user path and save the image
#         save_path = os.path.expanduser("~/1.png")
#         cv2.imwrite(save_path, frame)
#         # Save the image to the specified path, ensure the path is correct
#         break

# cap.release()
# cv2.destroyAllWindows()  # Release the window

# import cv2
# import os
# import numpy as np
# from matplotlib import pyplot as plt

# # Expand the user path to ensure the image path is correct
# image_path = os.path.expanduser("~/1.png")
# image = cv2.imread(image_path, 1)

# # Check if the image was successfully loaded
# if image is None:
#     print(f"Error: Unable to load image at {image_path}")
# else:
#     # Convert the image to HSV color space
#     HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define the mouse callback function
#     def getpos(event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDOWN:  # Define a left mouse button click event
#             print(HSV[y, x])

#     # Display the images
#     cv2.imshow("imageHSV", HSV)
#     cv2.imshow("image", image)
#     cv2.setMouseCallback("imageHSV", getpos)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# For realsense camera
import cv2
import os
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.bridge = CvBridge()
        self.image = None
        self.save_path = os.path.expanduser("~/1.png")

        # Initialize ROS node
        rospy.init_node('image_processor', anonymous=True)
        
        # Subscribe to the camera image topic
        self.rgb_sub = rospy.Subscriber("/camera_tb3_3/color/image_raw", Image, self.rgb_callback)

    def rgb_callback(self, data):
        try:
            # Convert the ROS Image message to a CV image
            self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def save_image(self):
        if self.image is not None:
            cv2.imwrite(self.save_path, self.image)

    def process_image(self):
        if self.image is None:
            print("No image data received yet.")
            return

        HSV = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        def getpos(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(HSV[y, x])

        cv2.imshow("imageHSV", HSV)
        cv2.imshow("image", self.image)
        cv2.setMouseCallback("imageHSV", getpos)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    processor = ImageProcessor()

    while not rospy.is_shutdown():
        if processor.image is not None:
            cv2.imshow("capture", processor.image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                processor.save_image()
                break

    processor.process_image()
    cv2.destroyAllWindows()
