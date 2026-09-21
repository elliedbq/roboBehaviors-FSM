import rclpy
from rclpy.node import Node
from threading import Thread, Event 
from time import sleep 
from geometry_msgs.msg import Twist 
import math 


class drive_square(Node):
    
    def __init__(self):
        super().__init__("drive_square_node")

        self.create_timer(1, self.run_loop)
        self.publisher = self.create_publisher(Twist, 'des_vel', 10)

    def run_loop(self):
        vel = Twist()
        self.publisher.publish(vel)
        print(vel)
        
        for _ in range(4):
            self.drive_forward(0.8)
            self.turn_left()
        print("square route completed")
        
    def drive(self, linear, angular):
        vel = Twist()
        vel.linear.x = linear
        vel.angular.z = angular 
        self.publisher.publish(vel)
        
    def drive_forward(self, distance):
        forward_vel = 0.3
        self.drive(linear = forward_vel, angular = 0.0)
        
        duration = distance / forward_vel
        sleep(duration)
        
        self.drive(linear = 0.0, angular = 0.0)
        
    def turn_left(self):
        angular_vel = 0.3
        self.drive(linear = 0.0, angular = angular_vel)
        sleep(math.pi/angular_vel/2) # 90 degree turn
        self.drive(linear= 0.0, angular = 0.0)
        sleep(0.5)
            
        
        
def main(args=None):
    """Initialize our node, run it, cleanup on shut down"""
    rclpy.init(args=args)  # Initialize ROS2 network
    node = drive_square()  # Create our node
    rclpy.spin(node)  # Run our node
    rclpy.shutdown()  # If interrupted, gracefully shutdown the ROS2 network

if __name__ == '__main__':
    main()
