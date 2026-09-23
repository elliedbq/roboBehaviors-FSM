"""create person following state"""
import rclpy
from rclpy.node import Node
from neato2_interfaces.msg import Bump
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import math as math
from time import sleep

class PersonFollowerNode(Node):
    """person follower node, inheriting from the rclpy Node class"""
    def __init__(self):
        """initialize person_follower_node. no inputs"""
        super().__init__('person_follower_node')

        self.state_active = False
        self.person_dist = 3
        self.person_dist2 = 0.2
        self.person_status = 'unknown'
        # options:  'head on' (head on to person) 
        #           'unknown' (need to find a person and go towards it)
        #           'at person' (at person, need to align to be straight)

        self.des_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.state_pub = self.create_publisher(String, 'state', 10)
        self.state_sub = self.create_subscription(String, 'state', self.process_state, 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.process_scan, 10)
        self.bump_sub = self.create_subscription(Bump, 'bump', self.process_bump, 10)
        print("Hey dere")


    def process_state(self,msg):
        """takes state msg and determines if person following state is active"""
        if msg.data == 'person_following':
            self.state_active = True
            self.person_status = 'unknown'
            print('person following state active')
        else:
            self.state_active = False


    def process_scan(self, msg):
        """takes msg input and sets person status"""
        
        if self.state_active:
            print('scanning')
            print(self.person_status)
            if self.person_status == 'unknown':
                print('finding person')
                self.find_person(msg)
            elif self.person_status == 'found_person' or self.person_status == 'looking_at_person':
                print('turning  and OR following  person')
                self.turn_to_person(msg)
        else:
            print('Bro im not on LOL')

            
    def find_person(self, msg):
        for i in range(0, len(msg.ranges) - 10, 5):
            if  self.person_dist2 < msg.ranges[i] < self.person_dist  \
                and msg.ranges[i+5] < self.person_dist \
                and msg.ranges[i+10] < self.person_dist:
                self.person_status = 'found_person'
                print('person found')
                break
            self.person_status = 'unknown'
            print('person not found')


    def turn_to_person(self, msg):
        # head on to person if side measurements line up
        # and there is NOT a person directly in front.
        print(f"msg.ranges[0]: {msg.ranges[0]} msg.ranges[350]: {msg.ranges[350]}")
        if self.person_dist2 > msg.ranges[0] or self.person_dist < msg.ranges[0]:
            print('person not ahead')
            self.send_velocity(0.0,10.0) # switched because we want to be right in front of person
            self.person_status = 'found_person'
        else:
            print('person ahead')
            self.send_velocity(0.1,0.0)
            self.person_status = 'looking_at_person'
            

    def send_velocity(self, linear, angle):
        """publishes desired velocity"""
        vel = Twist()
        vel.linear.x = linear
        vel.angular.z = math.radians(angle)
        self.des_vel_pub.publish(vel)

    def process_bump(self, msg):
        print('bump received')
        if msg.left_front == 1 and self.state_active:
            self.state_active = False
            send_msg = String()
            send_msg.data = 'square'
            self.state_pub.publish(send_msg)
            print('switch state to square')
            sleep(1)



def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)             # Initialize communication with ROS
    node = PersonFollowerNode()   # Create our Node
    rclpy.spin(node)                  # Run the Node until ready to shutdown
    rclpy.shutdown()                  # cleanup




if __name__ == '__main__':
    main()

