#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from cv_bridge import CvBridge
import cv2


# Webcam Subscriber node which inherits the Node parent class from rclpy
class gray(Node):

    rungray = True

    def __init__(self) -> None:
        super().__init__("gray_node") # Calling parents class to assign node name 
        self.get_logger().info("make image gray")
        self.subscription = self.create_subscription(  #Creating a subscription with a callback
            Image,
            'webcam_topic',
            self.listener_callback,
            10  # This number which you see in the C++ publisher nodes as well is the queue size, that is how many messages to keep in the queue (subscriber queue in this case). Any message that exceeds the queue will be dicarded
        )
        self.keybard = self.create_subscription (
            String,
            'keypress_topic',
            self.keypress_callback,
            10
        )
        self.bridge = CvBridge()  #Instantiating a CVBridge instance
        self.publisher = self.create_publisher(
            Image,
            'gray_image',
            10
        )

    #Callback function called when a message is ready to be processed from the subscriber queue
    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')  #Convert image to OpenCV matrix
        if self.rungray:
            cv_image = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY) #changes encoding, encoding in display.py is 'passthrough'
        cv_image = self.bridge.cv2_to_imgmsg(cv_image)
        self.publisher.publish(cv_image)
        cv2.waitKey(1)
    def keypress_callback(self, msg):
        tmp = msg.data
        print(f'keypress received: {tmp}')
        if(tmp=='K'):
            self.rungray = not self.rungray
    
# Main method is the first point of entry which instantiates an instance of the WebcamSubscriber class (a child of the Node class)
def main(args=None):
    rclpy.init()
    node = gray()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == "__main__":
    main()