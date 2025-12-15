---
sidebar_position: 4
---

# Assessment: ROS 2 Fundamentals

## Learning Objectives
After completing this assessment, you should be able to:
- Identify and explain the core components of ROS 2 architecture (nodes, topics, services, actions)
- Articulate at least 3 key differences and advantages of ROS 2 compared to ROS 1

## Questions

### 1. ROS 2 Architecture
Explain the purpose and function of each of the following ROS 2 components:
- Node
- Topic
- Service
- Action

### 2. ROS 2 vs ROS 1
List and describe at least 3 key differences between ROS 1 and ROS 2, explaining the advantages of each approach.

### 3. Communication Patterns
Describe when you would use topics, services, and actions in a robotics application. Provide an example for each.

### 4. Middleware
What is the role of DDS (Data Distribution Service) in ROS 2? Why was this chosen as the underlying middleware?

## Solutions

### 1. ROS 2 Architecture
- **Node**: A process that performs computation. Nodes are the fundamental building blocks of a ROS 2 system.
- **Topic**: A named bus over which nodes exchange messages. Topics support asynchronous, many-to-many communication.
- **Service**: A synchronous request/reply communication pattern between two nodes.
- **Action**: A communication pattern for long-running tasks with feedback, goal, and result.

### 2. ROS 2 vs ROS 1
- **Middleware**: ROS 2 uses DDS as its middleware, providing better scalability, real-time performance, and language independence.
- **Architecture**: ROS 2 uses a peer-to-peer discovery system instead of a central master, improving robustness.
- **Security**: ROS 2 includes built-in security features that were not available in ROS 1.

### 3. Communication Patterns
- **Topics**: Use for streaming data like sensor readings (e.g., camera images, LIDAR scans)
- **Services**: Use for request-response interactions (e.g., saving a map, changing a parameter)
- **Actions**: Use for long-running tasks with feedback (e.g., navigation to a goal, trajectory execution)

### 4. Middleware
DDS (Data Distribution Service) provides the underlying communication layer for ROS 2. It enables discovery, serialization, and transportation of messages between nodes, supporting real-time systems and offering multiple implementations for different use cases.