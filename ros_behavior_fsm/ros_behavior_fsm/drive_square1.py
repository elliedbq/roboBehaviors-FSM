import rclpy
from rclpy.node import Node
from time import sleep 
from geometry_msgs.msg import Twist 
import math 
from std_msgs.msg import String
from neato2_interfaces.msg import Bump
from threading import Thread, Event


class DriveSquare1Node(Node):
    
    def __init__(self):
        super().__init__("drive_square1_node")
        # not sure why drive square1 works while drive square does not
        # prob bc smth with the cache

        self.state_active = True

        self.bump_event = Event()

        self.publisher = self.create_publisher(Twist, 'des_vel', 10)
        self.state_sub = self.create_subscription(String, 'state', self.process_state, 10)
        self.state_pub = self.create_publisher(String, 'state', 10)
        self.bump_sub = self.create_subscription(Bump, 'bump', self.process_bump, 10)

        self.square_thread = Thread(target=self.run_loop)
        self.square_thread.start()

    def run_loop(self):
        while self.state_active:
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
        self.bump_event.wait(duration)
        
        self.drive(linear = 0.0, angular = 0.0)
        
    def turn_left(self):
        angular_vel = 0.3
        self.drive(linear = 0.0, angular = angular_vel)
        sleep(math.pi/angular_vel/2) # 90 degree turn
        self.drive(linear= 0.0, angular = 0.0)
        self.bump_event.wait(0.5)

    def process_state(self, msg):
        if msg.data == 'square':
            self.state_active = True
            self.bump_event.clear()
            self.square_thread = Thread(target=self.run_loop)
            self.square_thread.start()
        else:
            self.state_active = False

    def process_bump(self, msg):
        print('bump recieved')
        if msg.left_front == 1:
            self.state_active = False
            send_msg = String()
            send_msg.data = 'wall_following'
            self.state_pub.publish(send_msg)
            self.bump_event.set()
            print('switch state to wall following')
            sleep(1)
            
        
        
def main(args=None):
    """Initialize our node, run it, cleanup on shut down"""
    rclpy.init(args=args)  # Initialize ROS2 network
    node = DriveSquare1Node()  # Create our node
    rclpy.spin(node)  # Run our node
    rclpy.shutdown()  # If interrupted, gracefully shutdown the ROS2 network

if __name__ == '__main__':
    main()
