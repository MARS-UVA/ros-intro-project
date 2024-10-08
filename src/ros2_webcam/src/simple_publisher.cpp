#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
 
using namespace std::chrono_literals;
 
class WebcamPublisher : public rclcpp::Node {
public:
  WebcamPublisher()
    : Node("minimal_publisher"), count_(0)
    {
      publisher_ = this->create_publisher<std_msgs::msg::String>("chatter_topic", 10);
      timer_ = this->create_wall_timer(
      500ms, std::bind(&WebcamPublisher::timer_callback, this));
    }
 
private:
    void timer_callback()
    {
      auto message = std_msgs::msg::String();
      message.data = "Hello, world! " + std::to_string(count_++);
      RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
      publisher_->publish(message);
    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};
 
int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  // create a ros2 node
  auto node = std::make_shared<WebcamPublisher>();
 
  // process ros2 callbacks until receiving a SIGINT (ctrl-c)
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
