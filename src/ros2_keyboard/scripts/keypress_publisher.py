#!/usr/bin/env python3

import keyboard  #run 'pip install keyboard' in your terminal to get keyboard
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class KeypressPublisher(Node):
    def __init__(self):
        super().__init__('keypress_publisher')
        self.publisher_ = self.create_publisher(String, 'keypress_topic', 10) #Publisher for Python nodes that publishes messages of type String on the 'keypress_topic' topic and has a queue of 10 messages at a time
        self.read_timer = self.create_timer(0.1, self.read_keypress_callback)

    def read_keypress_callback(self):
        key_pressed = keyboard.read_event()
        msg = String()
        msg.data = f'{key_pressed.name}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published data: "{msg.data}"')

if __name__ == '__main__':
    rclpy.init()
    node = KeypressPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
