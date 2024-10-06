#!/usr/bin/env python3

# ROS Python Libraries
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# OpenCV imports, use 'pip install opencv-python' to get OpenCV for Python
from cv_bridge import CvBridge
import cv2

# Webcam Subscriber node which inherits the Node parent class from rclpy
class WebcamSubscriber(Node):
    def __init__(self):
        super().__init__("webcam_subscriber") # Calling parents class to assign node name 
        self.get_logger().info("Webcam subscriber node init")
        self.publisher_ = self.create_publisher(Image, 'image_topic', 10) #Publisher for Python nodes that publishes messages of type String on the 'keypress_topic' topic and has a queue of 10 messages at a time
        self.subscription = self.create_subscription(  #Creating a subscription with a callback
            Image,
            'webcam_topic',
            self.listener_callback,
            10  # This number which you see in the C++ publisher nodes as well is the queue size, that is how many messages to keep in the queue (subscriber queue in this case). Any message that exceeds the queue will be dicarded
        )
        self.bridge = CvBridge()  #Instantiating a CVBridge instance

    #Callback function called when a message is ready to be processed from the subscriber queue
    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')  #Convert image to OpenCV matrix
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        print(type(cv_image))
        cv2.imshow("Image", cv_image)
        cv2.waitKey(1)
        msg = self.bridge.cv2_to_imgmsg(cv_image)#, encoding='bgr8')
        

        self.publisher_.publish(msg)
        #self.get_logger().info(f'Published data: "{msg.data}"')
        #self.read_timer = self.create_timer(0.1, self.read_keypress_callback(cv_image))

        

    
# Main method is the first point of entry which instantiates an instance of the WebcamSubscriber class (a child of the Node class)
def main(args=None):
    rclpy.init()
    node = WebcamSubscriber()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
