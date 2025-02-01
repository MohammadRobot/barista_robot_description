
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_prefix, get_package_share_directory

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
    rviz_config_dir = os.path.join(get_package_share_directory(package_description), 'rviz', 'two_robot_vis.rviz')


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

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )    

    # # Position and orientation
    # # [X, Y, Z]
    # position = [0.0, 0.0, 0.2]
    # # [Roll, Pitch, Yaw]
    # orientation = [0.0, 0.0, 0.0]
    # # Base Name or robot
    # robot_base_name = "barista_robot"


    # entity_name = robot_base_name+"-"+str(int(random.random()*100000))


    robot_name_1 = "rick"
    robot_name_2 = "morty"

# Robot State Publisher
    rsp_robot1 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=robot_name_1,
        parameters=[{'frame_prefix': robot_name_1+'/', 'use_sim_time': use_sim_time,
                     'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', robot_name_1])}],
        output="screen"
    )

    rsp_robot2 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=robot_name_2,
        parameters=[{'frame_prefix': robot_name_2+'/', 'use_sim_time': use_sim_time,
                     'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', robot_name_2])}],
        output="screen"
    )
    

    # Spawn ROBOT Set Gazebo

    spawn_robot1 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robot1', '-x', '0.0', '-y', '0.0', '-z', '0.0',
                   '-topic', robot_name_1+'/robot_description']
    )

    spawn_robot2 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robot2', '-x', '2.0', '-y', '0.0', '-z', '0.0',
                   '-topic', robot_name_2+'/robot_description']
    )

    # Static transform world to odom
    static_tf_pub_1 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name="".join(['static_transform_publisher_', robot_name_1, '_odom']),
        output='screen',
        emulate_tty=True,
        arguments=['0', '0', '0', '0', '0', '0', 'world', robot_name_1 + '/odom'] # parent, child
    )

    static_tf_pub_2 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name="".join(['static_transform_publisher_', robot_name_2, '_odom']),
        output='screen',
        emulate_tty=True,
        arguments=['0', '0', '0', '0', '0', '0', 'world', robot_name_2 + '/odom'] # parent, child
    )

    # lunch RVIZ
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        name='rviz_node',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_dir])

    # create and return launch description object
    return LaunchDescription(
        [    
            DeclareLaunchArgument('world',
            default_value=[os.path.join(pkg_barista_robot_gazebo, 'worlds', 'barista_robot_empty.world'), ''],
            description='SDF world file'),        
            gazebo,
            rsp_robot1,
            rsp_robot2,
            spawn_robot1,
            spawn_robot2,
            static_tf_pub_1,
            static_tf_pub_2,
            rviz_node
        ]
    )