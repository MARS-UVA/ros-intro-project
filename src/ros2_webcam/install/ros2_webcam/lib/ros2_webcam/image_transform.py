#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

class ImageTransform(Node):
    def __init__(self):
        super().__init__('image_transform')
        self.publisher_ = self.create_publisher(Image, 'transformed_image_topic', 10)
        timer_period = 0.5  # seconds
        self.subscription = self.create_subscription(
            Image,
            'webcam_topic',
            self.image_callback,
            10
        )
        self.subscription = self.create_subscription(
            String,
            'keypress_topic',
            self.keypress_callback,
            10)
        self.bridge = CvBridge()
        self.greyscale = False
    def keypress_callback(self, msg):
        self.get_logger().info('Received keypress: "%s"' % msg.data)
        if msg.data == 'k':
            self.greyscale = not self.greyscale

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        if self.greyscale:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='mono8')
        else:
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
        self.publisher_.publish(ros_image)


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = ImageTransform()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()