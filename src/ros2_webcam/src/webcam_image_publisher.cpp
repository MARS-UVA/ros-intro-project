#include <chrono>
#include <functional>
#include <memory>
#include <string>

// Library that allows you  to interact with  ros2
#include "rclcpp/rclcpp.hpp"
// Library for Ros messages
#include "std_msgs/msg/string.hpp"
#include <opencv2/opencv.hpp>
#include <iostream>


#include <stdio.h>
#include "sensor_msgs/msg/image.hpp"
#include "cv_bridge/cv_bridge.h"
// for Size
#include <opencv2/core/types.hpp>
// for CV_8UC3
#include <opencv2/core/hal/interface.h>
// for compressing the image
#include <image_transport/image_transport.hpp>
#include <opencv2/imgproc/imgproc.hpp>
 
using namespace std::chrono_literals;
using namespace cv;
 
class WebcamVideoPublisher : public rclcpp::Node {
public:
  WebcamVideoPublisher()
    : Node("webcam_publisher"), count_(0)
    {
      publisher_ = this->create_publisher<sensor_msgs::msg::Image>("webcam_topic", 10);
      timer_ = this->create_wall_timer(500ms, std::bind(&WebcamVideoPublisher::timer_callback, this));
    }
 
private:
    void timer_callback()
    {
      cv_bridge::CvImagePtr cv_ptr;
      cv::Mat img(400, 400, CV_8UC3);
      cv::randu(img, Scalar(0, 0, 0), Scalar(255, 255, 255));

      sensor_msgs::msg::Image::SharedPtr msg = cv_bridge::CvImage(std_msgs::msg::Header(), "bgr8", img).toImageMsg();
      auto message = std_msgs::msg::String();
      message.data = "Publishing image frame " + std::to_string(count_++);
      RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
      publisher_->publish(*msg.get());
      std::cout << "Image frame published!" << std::endl;
    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
    size_t count_;
};
 
int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<WebcamVideoPublisher>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
