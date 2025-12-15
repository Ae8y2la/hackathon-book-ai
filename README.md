# Physical AI & Humanoid Robotics Educational Book

This repository contains an educational book on Physical AI & Humanoid Robotics, built with Docusaurus. The book provides comprehensive learning materials for connecting AI agents to humanoid robots using ROS 2.

## Modules

### Module 1: The Robotic Nervous System (ROS 2)

This module covers the fundamentals of ROS 2 for connecting AI agents to humanoid robots:

1. **ROS 2 Fundamentals**: Understanding the purpose of ROS 2 in physical AI, including concepts of nodes, topics, services, and actions, and how ROS 2 differs from ROS 1.

2. **Python Agents with ROS 2**: Learning how to create Python agents that connect to ROS 2 using rclpy, write ROS 2 Python nodes, implement topic-based robot control, and link AI logic to controllers.

3. **Humanoid Modeling with URDF**: Understanding URDF structure, creating links and joints, incorporating sensors, and applying humanoid modeling best practices.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hackathon-book-ai
   ```

2. Navigate to the website directory:
   ```bash
   cd website
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Start the development server:
   ```bash
   npm run start
   ```

The site will be available at http://localhost:3000

## Building for Production

To build the static files for deployment:

```bash
npm run build
```

The output will be in the `build/` directory and can be deployed to any static hosting service.

## Contributing

This project follows the specifications and plans defined in the `specs/` directory. All content is structured according to the established architecture and follows the quality standards defined in the project constitution.

## License

This educational material is provided under the terms defined in the project documentation.