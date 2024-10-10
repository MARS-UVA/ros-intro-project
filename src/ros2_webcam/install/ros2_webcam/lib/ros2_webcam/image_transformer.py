#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge


class MinimalPublisher(Node):

    def __init__(self):
        self.showGray = False
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Image, 'disp_topic', 10)
        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            String,
            'keypress_topic',
            self.keyboard_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.subscription2 = self.create_subscription(
            Image,
            'webcam_topic',
            self.webcam_callback,
            10)
        self.subscription2  # prevent unused variable warning

    def keyboard_callback(self, msg):
        self.get_logger().info("key was pressed")
        self.showGray = not self.showGray

    def webcam_callback(self, img):
        # transform image
        cv_image = self.bridge.imgmsg_to_cv2(img, desired_encoding='bgr8')  #Convert image to OpenCV matrix
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        # new_image = gray_image
        # if (not self.showGray):
        #     new_image = cv_image
        if (self.showGray):
            print("gray")
            self.publisher_.publish(self.bridge.cv2_to_imgmsg(gray_image, encoding='mono8'))
        else:
            print("color")
            self.publisher_.publish(img)
        # new_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='mono8')
        # self.publisher_.publish(new_image) # publish ros image


    

    

# class KeybSubscriber(Node):

#     def __init__(self):
#         super().__init__('keypress_subscriber')
#         self.subscription = self.create_subscription(
#             String,
#             'keyboard_topic',
#             self.listener2_callback,
#             10)
#         self.subscription  # prevent unused variable warning

#     def listener2_callback(self, msg):
#         self.get_logger().info('I heard: "%s"' % msg.data)

# class CamSubscriber(Node):

#     def __init__(self):
#         super().__init__('webcam_subscriber')
#         self.subscription = self.create_subscription(
#             String,
#             'webcam_topic',
#             self.listener_callback,
#             10)
#         self.subscription  # prevent unused variable warning

#     def listener_callback(self, msg):

#         self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()