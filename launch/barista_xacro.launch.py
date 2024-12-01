
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_prefix

import xacro


# this is the function launch  system will look for
def generate_launch_description():

    ####### DATA INPUT ##########
    # urdf_file = 'barista_robot_model.urdf'
    xacro_file = "barista_robot_model.urdf.xacro"
    package_description = "barista_robot_description"

    ####### DATA INPUT END ##########
    print("Fetching URDF ==>")
    # robot_desc_path = os.path.join(get_package_share_directory(package_description), "urdf", urdf_file)
    robot_desc_path = os.path.join(get_package_share_directory(package_description), "xacro", xacro_file)



    # RVIZ Configuration
    rviz_config_dir = os.path.join(get_package_share_directory(package_description), 'rviz', 'urdf_vis.rviz')


    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            name='rviz_node',
            parameters=[{'use_sim_time': True}],
            arguments=['-d', rviz_config_dir])

    # Gazebo Configration 
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_barista_robot_gazebo = get_package_share_directory('barista_robot_description')

    # We get the whole install dir
    # We do this to avoid having to copy or softlink manually the packages so that gazebo can find them
    description_package_name = "barista_robot_description"
    install_dir = get_package_prefix(description_package_name)

    # Set the path to the WORLD model files. Is to find the models inside the models folder in my_box_bot_gazebo package
    gazebo_models_path = os.path.join(pkg_barista_robot_gazebo, 'models')
    # os.environ["GAZEBO_MODEL_PATH"] = gazebo_models_path

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] =  os.environ['GAZEBO_MODEL_PATH'] + ':' + install_dir + '/share' + ':' + gazebo_models_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  install_dir + "/share" + ':' + gazebo_models_path

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'

    

    print("GAZEBO MODELS PATH=="+str(os.environ["GAZEBO_MODEL_PATH"]))
    print("GAZEBO PLUGINS PATH=="+str(os.environ["GAZEBO_PLUGIN_PATH"]))

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )    

    # Position and orientation
    # [X, Y, Z]
    position = [0.0, 0.0, 0.2]
    # [Roll, Pitch, Yaw]
    orientation = [0.0, 0.0, 0.0]
    # Base Name or robot
    robot_name = "barista_robot"


    entity_name = robot_name+"_"+str(int(random.random()*100000))

    # Robot State Publisher

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='my_robot_state_publisher_node',
        namespace=robot_name,
        emulate_tty=True,
        parameters=[{'use_sim_time': True,
                    'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', robot_name])}],
        output="screen"
    )

    # Spawn ROBOT Set Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=['-entity', entity_name,
                   '-x', str(position[0]), '-y', str(position[1]), '-z', str(position[2]),
                   '-R', str(orientation[0]), '-P', str(orientation[1]), '-Y', str(orientation[2]),
                   '-topic', robot_name+'/robot_description']
    )

    # create and return launch description object
    return LaunchDescription(
        [    
            DeclareLaunchArgument('world',
            default_value=[os.path.join(pkg_barista_robot_gazebo, 'worlds', 'barista_robot_empty.world'), ''],
            description='SDF world file'),        
            gazebo,
            robot_state_publisher_node,
            rviz_node,
            spawn_robot
        ]
    )