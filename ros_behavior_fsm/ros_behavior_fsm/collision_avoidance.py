""" Investigate receiving a message using a callback function """
import rclpy
from rclpy.node import Node
from neato2_interfaces.msg import Bump
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan

class CollisionAvoidanceNode(Node):
    """This is a message subscription node, which inherits from the rclpy Node class."""
    def __init__(self):
        """Initializes the collision_avoidance_node. No inputs."""
        super().__init__('collision_avoidance_node')

        self.create_timer(0.1, self.send_vel)

        self.target_stop = 0.2 # closest robot should get to the wall
        self.target_slow = 0.4 # when robot starts slowing down
        self.distance_to_obstacle = 0

        self.vel = Twist()
        self.bump_state = False
        self.bump_sub = self.create_subscription(Bump, 'bump', self.process_bump, 10)
        self.des_vel_sub = self.create_subscription(Twist, 'des_vel', self.process_des_vel, 10)

        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.process_scan, 10)

        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)


    def process_bump(self, msg):
        """sets bump state"""
        self.bump_state =  msg.left_front == 1 or msg.right_front == 1 or msg.left_side == 1 or msg.right_side == 1 

    def process_des_vel(self, msg):
        self.vel.linear.x = msg.linear.x
        self.vel.angular.z = msg.angular.z

    def process_scan(self, msg):
        if msg.ranges[0] != 0:
            self.distance_to_obstacle = msg.ranges[0]
        self.bump_state = False

    def send_vel(self):
        if self.bump_state == True:
            self.vel.linear.x = 0.0
            self.vel.angular.z = 0.0
            print('stopped bumped')

        # distance collision avoidance
        # elif self.distance_to_obstacle < self.target_stop:
        #     self.vel.linear.x = 0.0
        #     print('stopped close to wall')
        # elif self.distance_to_obstacle < self.target_slow:
        #     self.vel.linear.x = self.vel.linear.x/(self.target_slow - self.distance_to_obstacle)
        #     print('slowing down')



        self.cmd_vel_pub.publish(self.vel)
        print(str(self.vel.linear.x) + 'and' + str(self.vel.angular.z))


            



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
