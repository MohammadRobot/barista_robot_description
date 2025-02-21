
## Install Dependencies

```bash
sudo apt install ros-humble-xacro
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-gazebo-ros2-control
sudo apt install ros-humble-joint-state-broadcaster
sudo apt install ros-humble-joint-trajectory-controller
sudo apt install ros-humble-velocity-controllers
sudo apt install ros-humble-gazebo-plugins
```

## Build and Source the Package

```bash
cd ~/ros2_ws && colcon build && source install/setup.bash
```

## Run the Package

```bash
ros2 launch barista_robot_description barista_urdf.launch.py
ros2 launch barista_robot_description barista_xacro.launch.py
ros2 launch barista_robot_description barista_two_robots.launch.py
```

## Execute in Webshell 2 to Run `joint_state_publisher_gui`

```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

## Run `teleop_twist_keyboard` to Drive the Robot

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/barista_robot/cmd_vel
```

## Troubleshooting

- If the robots do not spawn in Gazebo, run:

```bash
gazebo --verbose

gazebo -s libgazebo_ros_init.so -s libgazebo_ros_factory.so myworld.world

```

- If you find the following warning:

```
[Wrn] [GuiIface.cc:120] QStandardPaths: wrong permissions on runtime directory /run/user/1000/, 0755 instead of 0700
```

- Run this command:

```bash
$ chmod 0700 /run/user/1000/
```

