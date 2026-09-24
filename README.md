# RoboBehaviors & Finite State Machine Project
Computational Robotics Project 1: Getting started with ROS.

Ellie Kung and Vanessa Aguilar Flores


Report:



## How to run
1. Download or clone our repository in your ROS workspace: `ros2_ws/src/`

2. Build and compile the packages:

        colcon build --symlink-install

3. Source the `install.bash` script:

        source ~/ros2_ws/install/setup.bash

4. Start the simulation world (works best with the left wall removed):

        ros2 launch neato2_gazebo neato_gauntlet_world.py

5. Run all behaviors:

        ros2 launch ros_behavior_fsm behaviors.launch.py

    Alternatively, run each node individually:

        ros2 run ros_behavior_fsm collision_avoidance
        ros2 run ros_behavior_fsm drive_square1
        ros2 run ros_behavior_fsm wall_follower
        ros2 run ros_behaviors_fsm person_follower

    To run bag files (located in `/bag-files`):

        ros2 bag play path-to-bag-file