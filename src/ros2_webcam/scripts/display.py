#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class WebcamSubscriber(Node):
    def __init__(self) -> None:
        super().__init__("webcam_subscriber")
        self.get_logger().info("Webcam subscriber node init")
        self.subscription = self.create_subscription(
            Image,
            'webcam_topic',
            self.listener_callback,
            10
        )
        self.bridge = CvBridge()
    
    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        cv2.imshow("Image", cv_image)
        cv2.waitKey(1)
    

def main(args=None):
    rclpy.init()
    node = WebcamSubscriber()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == "__main__":
    main()