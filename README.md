
Buiild and source the package

	cd ~/ros2_ws && colcon build && source install/setup.bash

Run the package

	ros2 launch barista_robot_description barista_urdf.launch.py

    ros2 launch barista_robot_description barista_xacro.launch.py

Execute in Webshell 2 to run joint_state_publisher_gui

	ros2 run joint_state_publisher_gui joint_state_publisher_gui


run teleop_twist_keyboard to drive the robot 
    ros2 run teleop_twist_keyboard teleop_twist_keyboard 

    ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/barista_robot/cmd_vel