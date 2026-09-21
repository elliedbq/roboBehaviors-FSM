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

        self.state_active = False
        self.wall_dist = 0.5
        self.wall_status = 'unknown'
        # options:  'parallel' (parallel to wall) 
        #           'unknown' (need to find a wall and go towards it)
        #           'at wall' (at wall, need to align to be straight)

        self.des_vel_pub = self.create_publisher(Twist, 'des_vel', 10)
        self.state_pub = self.create_publisher(String, 'state', 10)
        self.state_sub = self.create_subscription(String, 'state', self.process_state, 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.process_scan, 10)


    def process_state(self,msg):
        """takes state msg and determines if wall following state is active"""
        if msg.data == 'wall_following':
            self.state_active = True
            self.wall_status = 'unknown'
        else:
            self.state_active = False


    def process_scan(self, msg):
        """takes msg input and sets wall status"""
        if self.state_active:
            print('scanning')

            if self.wall_status == 'unknown':
                print('finding wall')
                self.find_wall(msg)
            elif self.wall_status == 'at_wall':
                print('becoming parallel')
                self.turn_to_wall(msg)
            else:
                print('following wall')
                self.follow_wall(msg)

            

    def find_distance(self, length, angle):
        """find normalized distance"""
        angle = math.radians(angle)
        return abs(length*math.sin(angle))

    def find_wall(self, msg):
        for i in range(0, len(msg.ranges) - 10, 5):
            if msg.ranges[i] < self.wall_dist \
                and msg.ranges[i+5] < self.wall_dist \
                and msg.ranges[i+10] < self.wall_dist:
                self.wall_status = 'at_wall'
                print('wall found')
                self.send_velocity(0.0,0.0) # stop once at wall
                return
        if abs(msg.ranges[10] - msg.ranges[350]) < 0.1 :
            # and abs(msg.ranges[20] - msg.ranges[340]) < 0.1: 
            # checks for wall in front of robot. (< 0.3 is in case of error in laser scans)
            self.send_velocity(0.1, 0.0) # if wall then go toward wall. if no wall, rotate.
        else:
            self.send_velocity(0.0, -10)

    def turn_to_wall(self, msg):
        # parallel to wall if side measurements line up
        # and there is NOT a wall directly in front.
        diff = msg.ranges[90] - self.find_distance(msg.ranges[100] ,100)
        print(msg.ranges[1])
        if msg.ranges[1] > (self.wall_dist) and abs(diff) < 0.005:
            print('parallel to wall')
            self.send_velocity(0.0,0.0)
            self.wall_status = 'parallel'
        else:
            self.send_velocity(0.0, 10)




    def follow_wall(self, msg):
        """tells robot to follows wall"""
        print('start function')
        if msg.ranges[1] < self.wall_dist*1.2:
            print('turn')
            self.send_velocity(0.0, -10)
        elif msg.ranges[90] < self.find_distance(msg.ranges[80], 80) or msg.ranges[90] > self.wall_dist:
            print('up')
            self.send_velocity(0.1, 10)
        elif msg.ranges[90] > self.find_distance(msg.ranges[80], 80):
            print('down')
            self.send_velocity(0.1, -10)
        else:
            print('straight')
            self.send_velocity(0.1, 0.0)

    def send_velocity(self, linear, angle):
        """publishes desired velcoity"""
        vel = Twist()
        vel.linear.x = linear
        vel.angular.z = math.radians(angle)
        self.des_vel_pub.publish(vel)

    def process_bump(self, msg):
        print('bump recieved')
        if msg.left_front == 1:
            self.state_active = False
            send_msg = String()
            send_msg.data = 'square'
            self.state_pub.publish(send_msg)
            print('switch state to square')



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

