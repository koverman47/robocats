cmake_minimum_required(VERSION 2.8.3)
add_compile_options(-std=c++11)
project(gazebo_robosub)

# Load catkin and all dependencies required for this package
find_package(catkin REQUIRED COMPONENTS 
  roscpp
  rospy
  gazebo_ros 
  std_msgs
  message_generation
)

# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

add_library(${PROJECT_NAME} src/motor_plugin.cpp)
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})



generate_messages(
	DEPENDENCIES
	std_msgs
)

#add_message_files(
#	FILES
#)

catkin_package(
  DEPENDS 
    roscpp 
    gazebo_ros 
)
