""" Investigate receiving a message using a callback function """
import rclpy
from rclpy.node import Node
from neato2_interfaces.msg import Bump
from geometry_msgs.msg import Twist 

class CollisionAvoidanceNode(Node):
    """This is a message subscription node, which inherits from the rclpy Node class."""
    def __init__(self):
        """Initializes the collision_avoidance_node. No inputs."""
        super().__init__('collision_avoidance_node')

        self.create_timer(0.1, self.send_vel)

        self.vel = Twist()
        self.bump_state = False
        self.sub = self.create_subscription(Bump, 'bump', self.process_bump, 10)
        self.sub = self.create_subscription(Twist, 'des_vel', self.process_des_vel, 10)

        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        self.send_vel()

    def process_bump(self, msg):
        """Takes msg input and prints the header of that message."""
        self.bump_state =  msg.left_front == 1 or msg.right_front == 1 or msg.left_side == 1 or msg.right_side == 1 

    def process_des_vel(self, msg):
        
        self.vel.linear.x = msg.linear.x

        

    def send_vel(self):
        if self.bump_state == True:
            self.vel.linear.x = 0.0
            print('stopped')
        self.publisher.publish(self.vel)
        print(self.vel.linear.x)


            



def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)             # Initialize communication with ROS
    node = CollisionAvoidanceNode()   # Create our Node
    rclpy.spin(node)                  # Run the Node until ready to shutdown
    rclpy.shutdown()                  # cleanup




if __name__ == '__main__':
    main()
