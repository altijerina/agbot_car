import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')     
    
    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                ' ',
                os.path.join(
                    get_package_share_directory("car_description"),
                    "urdf",
                    "car.xacro",
                ),
            ]
        ),
        value_type=str,
    )  

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description},
                    {'use_sim_time': use_sim_time}],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )  
    
    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["wheel_controller", 
                   "--controller-manager", 
                   "/controller_manager"],
    )    

    return LaunchDescription(
        [   
            robot_state_publisher_node, 
            joint_state_broadcaster_spawner,
            wheel_controller_spawner,
        ]
    )