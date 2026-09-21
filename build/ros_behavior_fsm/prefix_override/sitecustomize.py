import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ellie/ros2_ws/src/roboBehaviors-FSM/install/ros_behavior_fsm'
