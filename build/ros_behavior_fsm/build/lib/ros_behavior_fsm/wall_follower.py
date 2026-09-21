"""create wall following state"""
import rclpy
from rclpy.node import Node
from neato2_interfaces.msg import Bump
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import math as math

class WallFollowerNode(Node):
    """wall follower node, inheriting from the rclpy Node class"""
    def __init__(self):
        """initialize wall_wollower_node. no inputs"""
        super().__init__('wall_follower_node')

        self.state_active = True
        self.wall_status = 'unknown'
        # options:  'at wall' (parallel to wall) 
        #           'turning' (next to wall but at edge, need to turn) 
        #           'unknown' (need to find a wall and go towards it)
        #           'toward wall' (going straight toward wall)
        #           'at wall' (at wall, need to align to be straight)

        self.des_vel_pub = self.create_publisher(Twist, 'des_vel', 10)

        self.state_sub = self.create_subscription(String, 'state', self.process_state, 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.process_scan, 10)

        if self.state_active:
            self.create_timer(0.1, self.follow_wall)

    def process_state(self,msg):
        """takes state msg and determines if wall following state is active"""
        if msg.string == 'wall_following':
            self.state_active = True
        else:
            self.state_active = False


    def process_scan(self, msg):
        """takes msg input and sets wall status"""
        # if parallel to wall
        if math.abs(self.find_distance(msg.ranges[80], 80) - self.find_distance(msg.ranges[100],100)) \
        == 0.1 \
        and self.find_distance(msg.ranges[90],90) == 0.3:
            self.send_velocity(0)
        elif self.find_distance(msg.ranges[90],90) > self.find_distance(msg.ranges[100],100) or \
            self.find_distance(msg.ranges[90],90) < 0.3:
            self.send_velocity(0.1)
        elif self.find_distance(msg.ranges[90], 90) < self.find_distance(msg.ranges[100],100) or \
            self.find_distance(msg.ranges[90],90) > 0.3:
            self.send_velocity(-0.1)
        
            

    def find_distance(self, length, angle):
        """find normalized distance"""
        angle = math.radians(angle)
        return length*math.cos(angle)


    def follow_wall(self):
        """tells robot to follows wall"""
        if self.wall_status == 'at wall':
            self.send_velocity(0)

    def send_velocity(self, angle):
        """publishes desired velcoity"""
        vel = Twist()
        if angle == 0:
            vel.linear.x = 0.1
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.x = angle

        self.des_vel_pub.publish(vel)




def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)             # Initialize communication with ROS
    node = WallFollowerNode()   # Create our Node
    rclpy.spin(node)                  # Run the Node until ready to shutdown
    rclpy.shutdown()                  # cleanup




if __name__ == '__main__':
    main()

