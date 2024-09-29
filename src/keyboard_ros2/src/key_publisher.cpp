#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include <iostream>
#include <termios.h>
#include <unistd.h>

class KeyboardListener : public rclcpp::Node {
public:
    KeyboardListener()
        : Node("keyboard_listener") {
        publisher_ = this->create_publisher<std_msgs::msg::String>("keypress_topic", 10);
        RCLCPP_INFO(this->get_logger(), "Press any key to change yoru webcam frame...");

        keyboard_thread_ = std::thread(&KeyboardListener::read_keyboard, this);
    }

    ~KeyboardListener() {
        if (keyboard_thread_.joinable()) {
            keyboard_thread_.join();
        }
    }

private:
    void read_keyboard() {
        char c;
        while (rclcpp::ok()) {
            c = get_key();
            if (c == 'q') {
                rclcpp::shutdown();
                break;
            }
            auto message = std_msgs::msg::String();
            message.data = std::string(1, c);
            publisher_->publish(message);
            RCLCPP_INFO(this->get_logger(), "Key pressed: %c", c);
        }
    }

    char get_key_press() {
        struct termios oldt, newt;
        char c;
        tcgetattr(STDIN_FILENO, &oldt);
        newt = oldt;
        newt.c_lflag &= ~(ICANON | ECHO);
        tcsetattr(STDIN_FILENO, TCSANOW, &newt);
        c = getchar();
        tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
        return c;
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    std::thread keyboard_thread_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<KeyboardListener>());
    rclcpp::shutdown();
    return 0;
}

