---
sidebar_position: 3
---

# Chapter 3: Humanoid Modeling with URDF

## Introduction to URDF

Unified Robot Description Format (URDF) is an XML format used to describe robots in ROS. It defines the physical and visual properties of a robot, including its links, joints, inertial properties, visual meshes, and collision properties. URDF is essential for robot simulation, visualization, and kinematic analysis.

## URDF Structure

A URDF file is an XML document with a `<robot>` root element that contains:

- **Links**: Represent rigid bodies with visual, collision, and inertial properties
- **Joints**: Define connections between links with specific degrees of freedom
- **Materials**: Define visual appearance properties
- **Gazebos**: Define simulation-specific properties

### Basic Robot Structure

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Links -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.25"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.25"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0.25 -0.125" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.125" length="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```

## Links

Links represent rigid bodies in the robot. Each link can have:

- **Visual**: How the link appears in visualizers
- **Collision**: How the link interacts in collision detection
- **Inertial**: Physical properties for simulation

### Visual Properties

```xml
<link name="link_name">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <!-- Choose one geometry type -->
      <box size="1 1 1"/>
      <!-- OR -->
      <cylinder radius="0.5" length="1.0"/>
      <!-- OR -->
      <sphere radius="0.5"/>
      <!-- OR -->
      <mesh filename="package://my_robot/meshes/link.stl"/>
    </geometry>
    <material name="color">
      <color rgba="0.8 0.2 0.2 1.0"/>
    </material>
  </visual>
</link>
```

### Collision Properties

```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <!-- Similar to visual but often simplified for performance -->
    <box size="1 1 1"/>
  </geometry>
</collision>
```

### Inertial Properties

```xml
<inertial>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <mass value="1.0"/>
  <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
</inertial>
```

## Joints

Joints connect links and define their relative motion. Common joint types:

- **fixed**: No movement (0 DOF)
- **revolute**: Single axis rotation with limits (1 DOF)
- **continuous**: Single axis rotation without limits (1 DOF)
- **prismatic**: Single axis translation with limits (1 DOF)
- **planar**: Movement in a plane (2 DOF)
- **floating**: Free movement in 3D space (6 DOF)

### Joint Definition

```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link_name"/>
  <child link="child_link_name"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  <dynamics damping="0.1" friction="0.0"/>
</joint>
```

## Sensors in URDF

Sensors are represented as special links with Gazebo plugins:

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.05 0.05 0.05"/>
    </geometry>
  </visual>
</link>

<gazebo reference="camera_link">
  <sensor type="camera" name="camera1">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## Humanoid Modeling Best Practices

### Kinematic Chain Structure

For humanoid robots, follow a standard structure:

```
base_link (or pelvis)
├── torso
│   ├── head
│   │   └── camera/sensors
│   ├── left_upper_arm
│   │   ├── left_lower_arm
│   │   └── left_hand
│   └── right_upper_arm
│       ├── right_lower_arm
│       └── right_hand
├── left_upper_leg
│   ├── left_lower_leg
│   └── left_foot
└── right_upper_leg
    ├── right_lower_leg
    └── right_foot
```

### Example Humanoid URDF Fragment

```xml
<!-- Pelvis/Root -->
<link name="pelvis">
  <visual>
    <geometry>
      <box size="0.25 0.15 0.2"/>
    </geometry>
    <material name="gray">
      <color rgba="0.5 0.5 0.5 1"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.25 0.15 0.2"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="5"/>
    <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.2" iyz="0" izz="0.15"/>
  </inertial>
</link>

<!-- Spine -->
<joint name="torso_joint" type="revolute">
  <parent link="pelvis"/>
  <child link="torso"/>
  <origin xyz="0 0 0.15" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-0.5" upper="0.5" effort="100" velocity="1"/>
</joint>

<link name="torso">
  <visual>
    <geometry>
      <box size="0.2 0.15 0.3"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.2 0.15 0.3"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="4"/>
    <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.15" iyz="0" izz="0.1"/>
  </inertial>
</link>

<!-- Hip joint for left leg -->
<joint name="left_hip_joint" type="revolute">
  <parent link="pelvis"/>
  <child link="left_thigh"/>
  <origin xyz="-0.07 0.08 -0.1" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="0.785" effort="200" velocity="1"/>
</joint>

<link name="left_thigh">
  <visual>
    <geometry>
      <cylinder length="0.4" radius="0.05"/>
    </geometry>
    <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
  </visual>
  <collision>
    <geometry>
      <cylinder length="0.4" radius="0.05"/>
    </geometry>
    <origin xyz="0 0 -0.2" rpy="1.57 0 0"/>
  </collision>
  <inertial>
    <mass value="2"/>
    <inertia ixx="0.05" ixy="0" ixz="0" iyy="0.05" iyz="0" izz="0.001"/>
  </inertial>
</link>
```

## Exercises

### Exercise 1: Simple Robot Model
Create a URDF model of a simple wheeled robot with a base and two wheels.

### Exercise 2: Manipulator Arm
Create a URDF model of a 3-DOF manipulator arm with proper joints and links.

### Exercise 3: Humanoid Body Part
Create a URDF model of a humanoid leg with hip, knee, and ankle joints.

## References

Smart, W. D., et al. (2012). URDF: Unified Robot Description Format. *Robotics: Science and Systems Conference*.

ROS.org. (2023). *URDF Tutorials*. https://wiki.ros.org/urdf/Tutorials

Khatib, O., et al. (2018). Robot modeling with URDF. *IEEE Robotics & Automation Magazine*, 25(3), 18-29.

## Summary

URDF provides a standardized way to describe robot models in ROS. Understanding how to create proper URDF files with correct links, joints, and physical properties is essential for humanoid robot modeling. This chapter covered the basic structure of URDF files, how to define links and joints, how to incorporate sensors, and best practices for humanoid modeling.

With this knowledge, you can now create complete robot models that can be used in simulation, visualization, and control systems.