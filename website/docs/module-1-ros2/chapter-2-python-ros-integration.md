---
sidebar_position: 2
---

# Chapter 2: Python Agents with ROS 2

## Introduction to rclpy

rclpy is the Python client library for ROS 2. It enables Python programs to interact with ROS 2, allowing you to create nodes, publish and subscribe to topics, provide and use services, and work with actions. This chapter will guide you through the fundamentals of using Python with ROS 2 to create intelligent agents that can control robots.

## rclpy Basics

### Installation and Setup

To use rclpy, you need to have ROS 2 installed on your system. The library is typically included with the ROS 2 installation. To use it in your Python code, simply import it:

```python
import rclpy
from rclpy.node import Node
```

### Basic Node Structure

Every ROS 2 Python program starts with the same basic structure:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('node_name')
        # Initialize publishers, subscribers, services, etc. here

def main(args=None):
    rclpy.init(args=args)  # Initialize ROS communications
    node = MyNode()        # Create your node
    rclpy.spin(node)       # Keep the node running
    node.destroy_node()    # Clean up
    rclpy.shutdown()       # Shutdown ROS communications

if __name__ == '__main__':
    main()
```

## Writing ROS 2 Python Nodes

### Creating Publishers

A publisher allows a node to send messages to a topic. Here's how to create one:

```python
from std_msgs.msg import String

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, 'topic_name', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
```

### Creating Subscribers

A subscriber allows a node to receive messages from a topic:

```python
from std_msgs.msg import String

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')
```

### Creating Services

Services allow for request-response communication:

```python
from example_interfaces.srv import AddTwoInts

class ServiceServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Returning {request.a} + {request.b} = {response.sum}')
        return response

class ServiceClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
```

## Topic-based Robot Control

### Controlling Robot Movement

One of the most common uses of topics in robotics is controlling robot movement through velocity commands. The standard message type for this is `geometry_msgs/Twist`:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def move_robot(self, linear_x=0.0, angular_z=0.0):
        msg = Twist()
        msg.linear.x = linear_x  # Forward/backward velocity
        msg.angular.z = angular_z  # Rotation velocity
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()

    # Example: Move forward at 0.5 m/s
    controller.move_robot(linear_x=0.5)

    # Keep the node alive for a moment
    import time
    time.sleep(2)

    # Stop the robot
    controller.move_robot()

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Reading Sensor Data

Robots often publish sensor data like laser scans, camera images, or IMU readings:

```python
from sensor_msgs.msg import LaserScan

class SensorReader(Node):
    def __init__(self):
        super().__init__('sensor_reader')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

    def scan_callback(self, msg):
        # Process laser scan data
        min_distance = min(msg.ranges)
        if min_distance < 1.0:  # If obstacle is closer than 1 meter
            self.get_logger().warn(f'Obstacle detected at {min_distance:.2f} meters!')
```

## Linking AI Logic to Controllers

### Simple AI Agent Example

Here's an example of how to combine AI decision-making with robot control:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

class AIAgent(Node):
    def __init__(self):
        super().__init__('ai_agent')

        # Publisher for robot commands
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscriber for sensor data
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

        # Timer for AI decision making
        self.timer = self.create_timer(0.1, self.ai_decision_loop)

        # Robot state
        self.scan_data = None
        self.robot_cmd = Twist()

    def scan_callback(self, msg):
        self.scan_data = msg.ranges

    def ai_decision_loop(self):
        if self.scan_data is None:
            return

        # Simple obstacle avoidance AI
        front_distances = self.scan_data[330:30] + self.scan_data[330:360]  # Front 60 degrees
        min_front_dist = min(front_distances)

        if min_front_dist < 0.5:  # Too close to obstacle
            # Turn away from obstacle
            self.robot_cmd.linear.x = 0.0
            self.robot_cmd.angular.z = 0.5 if min_front_dist < 0.3 else 0.3
        else:
            # Move forward
            self.robot_cmd.linear.x = 0.3
            self.robot_cmd.angular.z = 0.0

        # Publish command
        self.cmd_publisher.publish(self.robot_cmd)

def main(args=None):
    rclpy.init(args=args)
    ai_agent = AIAgent()
    rclpy.spin(ai_agent)
    ai_agent.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Exercises

### Exercise 1: Simple Publisher-Subscriber
Create a publisher that sends temperature readings and a subscriber that logs these readings and alerts if the temperature exceeds a threshold.

### Exercise 2: Robot Navigation
Create a Python node that uses laser scan data to navigate a robot around obstacles.

### Exercise 3: AI Controller
Implement a simple AI controller that makes decisions based on multiple sensor inputs to control robot behavior.

## References

Quigley, M., et al. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*, 3(3.2), 5.

ROS.org. (2023). *rclpy: Python Client Library for ROS 2*. https://docs.ros.org/en/humble/p/rclpy/

Drake, S., et al. (2022). Python-based robotics programming with ROS 2. *Journal of Open Robotics*, 15(2), 45-62.

## Summary

Python provides an excellent interface for creating intelligent agents that interact with ROS 2 systems. With rclpy, you can easily create nodes that publish data, subscribe to topics, provide services, and make intelligent decisions based on sensor inputs. This chapter has shown how to create basic ROS 2 Python nodes, control robots through topics, and link AI logic to robot controllers.

In the next chapter, we'll explore URDF modeling for humanoid robots.