import rclpy 
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class goStraightNode(Node):
    def __init__(self):
        super().__init__("go_straight_node")
        self.state_active = False

        if self.state_active:
            self.create_timer(0.1, self.run_loop)

        self.publisher = self.create_publisher(Twist, 'des_vel', 10)
        self.state_sub = self.create_subscription(String, 'state', self.process_state, 10)

    def run_loop(self):
        vel = Twist()
        vel.linear.x = 0.1
        self.publisher.publish(vel)
        print(vel)

    def process_state(self, msg):
        if msg.data == 'straight':
            self.state_active = True
        else:
            self.state_active = False


def main(args=None):
    """Initialize our node, run it, cleanup on shut down"""
    rclpy.init(args=args)  # Initialize ROS2 network
    node = goStraightNode()  # Create our node
    rclpy.spin(node)  # Run our node
    rclpy.shutdown()  # If interrupted, gracefully shutdown the ROS2 network

if __name__ == '__main__':
    main()

