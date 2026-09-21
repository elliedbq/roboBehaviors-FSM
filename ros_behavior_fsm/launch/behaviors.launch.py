from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        Node(
            package='ros_behavior_fsm',
            executable='collision_avoidance',
            output='screen'
        ),

        Node(
            package='ros_behavior_fsm',
            executable='wall_follower',
            output='screen'
        ),

        Node(
            ackage='ros_behavior_fsm',
            executable='drive_square1',
            output='screen'
        )

    ])