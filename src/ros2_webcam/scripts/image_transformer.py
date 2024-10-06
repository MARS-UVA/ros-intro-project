#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from cv_bridge import CvBridge
import cv2

class Image_Transformer(Node):
    def __init__(self):
        super().__init__('image_transform')
        WebcamData = self.subscription = self.create_subscription(
            Image,
            'webcam_topic',
            self.handleImage,
            10)
        KeyboardData = self.subscription = self.create_subscription(
            String,
            'keyboard_topic',
            self.handleKeyPress,
            10)
        self.publisher = self.create_publisher(Image, 'transformed_image', 10)
        self.isGrayscale = False
        self.bridge = CvBridge()

    def handleImage(self,msg):
        if(self.isGrayscale):
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono16')
            cv_image = self.bridge.cv2_to_imgmsg(cv_image, desired_encoing = 'mono16')
        else:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            cv_image = self.bridge.cv2_to_imgmsg(cv_image, desired_encoing = 'passthrough')
        #newMsg = $msg but grayscale
        self.publisher.publish(cv_image)
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')  #Convert image to OpenCV matrix
        cv2.imshow("Image", cv_image)
        cv2.waitKey(1)

    def handleKeyPress(self,msg):
        if(msg == "k"):
            self.isGrayscale = not self.isGrayscale
        

def main(args=None):
    rclpy.init()
    node = WebcamSubscriber()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    rclpy.shutdown()