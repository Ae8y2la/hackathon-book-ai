---
sidebar_position: 1
---

# Chapter 1: ROS 2 Fundamentals

## Introduction to ROS 2

Robot Operating System 2 (ROS 2) is a flexible framework for writing robot applications. It is a collection of software libraries and tools that help you build robot applications. From drivers to state estimation to planning, control, and more, ROS 2 provides the components you need to build your robot application.

ROS 2 is not an operating system, but rather a middleware framework that provides services designed for a heterogeneous computer cluster. It includes hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.

## Purpose of ROS 2 in Physical AI

ROS 2 serves as the middleware layer that connects AI agents to physical robots. It provides a standardized communication framework that allows:

- **Decoupled Development**: AI researchers can focus on algorithms while robotics engineers handle hardware integration
- **Reusability**: Components can be reused across different robot platforms
- **Scalability**: Systems can be distributed across multiple machines
- **Real-time Communication**: Low-latency communication between AI decision-making and robot execution

In the context of Physical AI and humanoid robotics, ROS 2 enables AI agents to control robot behavior, process sensor data, and interact with the physical world in a structured and standardized way.

## Core Architecture Concepts

### Nodes

A node is a process that performs computation. Nodes are the fundamental building blocks of a ROS 2 system. Each node should perform a specific, modular function (e.g., controlling a wheel, processing camera images, etc.). Multiple nodes work together to form a complete robot application.

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Hello from my_node!')

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Topics

Topics enable asynchronous, many-to-many communication between nodes. Nodes can publish messages to a topic or subscribe to a topic to receive messages. This creates a decoupled communication pattern where publishers and subscribers don't need to know about each other.

```python
# Publisher example
publisher = self.create_publisher(String, 'topic_name', 10)

# Subscriber example
subscriber = self.create_subscription(
    String,
    'topic_name',
    self.listener_callback,
    10
)
```

### Services

Services provide synchronous request/reply communication between two nodes. A service client sends a request to a service server, which processes the request and sends back a response. This is useful for operations that require a direct response.

```python
# Service server
service = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

# Service client
client = self.create_client(AddTwoInts, 'add_two_ints')
```

### Actions

Actions are used for long-running tasks that require feedback, goal management, and result reporting. They combine the benefits of topics (for feedback) and services (for goals and results) in a single communication pattern.

## ROS 2 vs ROS 1

ROS 2 was developed to address limitations of ROS 1 and provide a more robust, scalable, and production-ready framework:

### Key Differences

1. **Middleware**:
   - ROS 1: Uses a custom TCPROS/UDPROS transport layer with a central master
   - ROS 2: Uses DDS (Data Distribution Service) as the underlying middleware, providing better scalability, real-time performance, and language independence

2. **Architecture**:
   - ROS 1: Relies on a central master for name resolution and discovery
   - ROS 2: Uses a peer-to-peer discovery system, making it more robust and suitable for distributed systems

3. **Security**:
   - ROS 1: No built-in security features
   - ROS 2: Includes built-in security features like authentication, access control, and encryption

4. **Real-time Support**:
   - ROS 1: Limited real-time capabilities
   - ROS 2: Better support for real-time systems with deterministic communication

5. **Multi-robot Systems**:
   - ROS 1: Complex to set up for multi-robot scenarios
   - ROS 2: Natively supports multi-robot systems and distributed computing

6. **Quality of Service (QoS)**:
   - ROS 2 introduces QoS settings that allow fine-tuning communication behavior based on application requirements

## Exercises

### Exercise 1: Node Creation
Create a simple ROS 2 node that publishes "Hello, World!" messages to a topic called "greetings" at a rate of 1 Hz.

**Solution**:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class GreetingPublisher(Node):
    def __init__(self):
        super().__init__('greeting_publisher')
        self.publisher = self.create_publisher(String, 'greetings', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello, World! {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    greeting_publisher = GreetingPublisher()
    rclpy.spin(greeting_publisher)
    greeting_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Exercise 2: Topic Communication
Create a publisher node that publishes integer messages to a topic and a subscriber node that receives and prints these messages.

### Exercise 3: Service Implementation
Implement a simple service that adds two integers together. Create both the service server and a client that calls the service.

## Summary

ROS 2 provides a robust middleware framework that enables the development of complex robotic applications by standardizing communication between different components. Its architecture based on nodes, topics, services, and actions allows for modular, decoupled development that is essential for connecting AI agents to physical robots.

## References

Open Robotics. (2023). *ROS 2 Documentation*. Open Robotics. https://docs.ros.org/en/humble/

Quigley, M., Gerkey, B., & Smart, W. D. (2009). ROS: An open-source Robot Operating System. *ICRA Workshop on Open Source Software*, 3(3.2), 5.

Steinhorst, S., & Chitta, S. (2021). ROS 2 for dummies. *IEEE Control Systems Magazine*, 41(6), 16-30.

Sünderhauf, N., et al. (2018). On lifelong learning and modularizing deployment in robotics. *arXiv preprint arXiv:1803.04053*.

ROS Industrial Consortium. (2022). *ROS-Industrial Training Materials*. ROS-Industrial Consortium. https://rosindustrial.org/training/

In the next chapter, we'll explore how to implement Python agents that interface with ROS 2 using the rclpy client library.