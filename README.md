
## install Dependencies

    $ sudo apt install ros-humble-xacro

    $ sudo apt install ros-humble-ros2-control

    $ sudo apt install ros-humble-gazebo-ros2-control

    $ sudo apt install ros-humble-joint-state-broadcaster

    $ sudo apt install ros-humble-joint-trajectory-controller

    $ sudo apt install ros-humble-velocity-controllers

    $ sudo apt install ros-humble-gazebo-plugins



Buiild and source the package

	cd ~/ros2_ws && colcon build && source install/setup.bash

Run the package

	ros2 launch barista_robot_description barista_urdf.launch.py

    ros2 launch barista_robot_description barista_xacro.launch.py

    ros2 launch barista_robot_description barista_two_robots.launch.py

Execute in Webshell 2 to run joint_state_publisher_gui

	ros2 run joint_state_publisher_gui joint_state_publisher_gui


run teleop_twist_keyboard to drive the robot 
    ros2 run teleop_twist_keyboard teleop_twist_keyboard 

    ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/barista_robot/cmd_vel


## Trablshooting 

- if the robots not spawn in Gazebo run '$ gazebo --verbose'

    - if you find the follwing Worning: 

    [Wrn] [GuiIface.cc:120] QStandardPaths: wrong permissions on runtime directory /run/user/1000/, 0755 instead of 0700

    - run this command '$ chmod 0755  /run/user/1000/'

