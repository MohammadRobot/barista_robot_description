
Buiild and source the package

	cd ~/ros2_ws && colcon build && source install/setup.bash

Run the package

	ros2 launch barista_robot_description barista_urdf.launch.py

Execute in Webshell 2

	ros2 run joint_state_publisher_gui joint_state_publisher_gui