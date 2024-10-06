#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
class ImageTransform(Node):
    def __init__(self):
        super().__init__('image_transform')
        self.publisher = self.create_publisher(Image, 'transformed_images', 10)
        self.imageSubscription = self.create_subscription(
            Image,
            'webcam_topic',
            self.handleImage,
            10)
        self.keyPressSubscription = self.create_subscription(
            String,
            'keypress_topic',
            self.handleKeyPress,
            10)
        self.isGrayScale = False
        self.bridge = CvBridge() 
    def handleImage(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        if self.isGrayScale:
        
            newMsg = self.bridge.cv2_to_imgmsg(cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY), desired_encoding = "bgr8")
        else:
            newMsg = msg
        self.publisher.publish(newMsg)
    def handleKeyPress(self, msg):
        if msg.data == "k":
            self.isGrayScale = not self.isGrayScale

def main(args=None):
    rclpy.init(args=args)

    imgTransformNode = ImageTransform()

    rclpy.spin(imgTransformNode)
    imgTransformNode.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()