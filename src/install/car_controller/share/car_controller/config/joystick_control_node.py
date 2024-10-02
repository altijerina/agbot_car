# joystick_control_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoystickControlNode(Node):
    def __init__(self):
        super().__init__('joystick_control_node')
        
        # Create a publisher for cmd_vel (robot's velocity commands)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Create a subscription to the joystick topic
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10
        )
        
    def joy_callback(self, msg):
        twist = Twist()
        
        # Map joystick axes to linear and angular velocities
        twist.linear.x = msg.axes[1]  # Forward/backward
        twist.angular.z = msg.axes[0]  # Left/right
        
        # Publish the twist message
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = JoystickControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
