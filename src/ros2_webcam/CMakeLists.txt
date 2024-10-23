cmake_minimum_required(VERSION 3.8)
project(ros2_webcam)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(OpenCV REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
include_directories(include)

#add_executable(cam_pub src/simple_publisher.cpp)
#add_executable(cam_sub src/simple_subscriber.cpp)
add_executable(webcam_pub src/webcam_image_publisher.cpp)
target_link_libraries(webcam_pub ${OpenCV_LIBS})
target_include_directories(webcam_pub PRIVATE ${OpenCV_INCLUDE_DIRS})
#ament_target_dependencies(cam_pub rclcpp std_msgs sensor_msgs cv_bridge image_transport OpenCV)
#ament_target_dependencies(cam_sub rclcpp std_msgs sensor_msgs cv_bridge image_transport OpenCV)
ament_target_dependencies(webcam_pub rclcpp std_msgs sensor_msgs cv_bridge image_transport OpenCV)

install(TARGETS
 #cam_pub
 # cam_sub
  webcam_pub
  DESTINATION lib/${PROJECT_NAME})


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_python_install_package(${PROJECT_NAME})
install(PROGRAMS
  scripts/display.py
  scripts/image_transform.py
  DESTINATION lib/${PROJECT_NAME})

ament_package()

