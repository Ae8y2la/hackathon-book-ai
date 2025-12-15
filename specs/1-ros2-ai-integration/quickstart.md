# Quickstart Guide: Module 1 — The Robotic Nervous System (ROS 2)

**Feature**: 1-ros2-ai-integration
**Date**: 2025-12-15

## Prerequisites

Before starting this module, ensure you have:

- Node.js version 18 or higher installed
- npm or yarn package manager
- Git for version control
- A GitHub account (for deployment)
- Intermediate Python knowledge (comfortable with syntax and virtual environments)
- Basic AI concepts understanding (agents, decision logic)

## Setup Docusaurus Project

### 1. Clone or Create the Repository
```bash
# If you're working in an existing repository, skip this step
# Otherwise, create a new directory for your project
mkdir physical-ai-book
cd physical-ai-book
```

### 2. Install Docusaurus
```bash
# Create a new Docusaurus project
npx create-docusaurus@latest website classic

# Navigate to the project directory
cd website
```

### 3. Install Additional Dependencies
```bash
# No additional dependencies required for basic setup
# All necessary packages come with the classic template
```

## Project Structure

After setup, your project structure should look like:

```
website/
├── blog/                 # Blog posts (optional)
├── docs/                 # Documentation files
│   └── intro.md
├── src/
│   ├── components/       # React components
│   ├── css/              # Custom styles
│   └── pages/            # Standalone pages
├── static/               # Static assets
├── docusaurus.config.js  # Main configuration file
├── package.json
├── sidebar.js           # Sidebar configuration
└── README.md
```

## Adding Module Content

### 1. Create Module Directory
```bash
mkdir docs/module-1-ros2
```

### 2. Create Chapter Files
```bash
# Create the three required chapters
touch docs/module-1-ros2/chapter-1-ros2-fundamentals.md
touch docs/module-1-ros2/chapter-2-python-ros-integration.md
touch docs/module-1-ros2/chapter-3-urdf-modeling.md
```

### 3. Update Sidebar Configuration
Edit `sidebar.js` to include the new module and chapters:

```javascript
// sidebars.js
module.exports = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1 — The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-ros2/chapter-1-ros2-fundamentals',
        'module-1-ros2/chapter-2-python-ros-integration',
        'module-1-ros2/chapter-3-urdf-modeling',
      ],
    },
  ],
};
```

## Running the Development Server

### 1. Start the Development Server
```bash
npm run start
```

This will start the development server at `http://localhost:3000`.

### 2. View Your Content
Open your browser and navigate to `http://localhost:3000` to see your documentation site.

## Adding Content to Chapters

### Chapter 1: ROS 2 Fundamentals
Add content to `docs/module-1-ros2/chapter-1-ros2-fundamentals.md`:

```markdown
---
sidebar_position: 1
---

# Chapter 1: ROS 2 Fundamentals

## Introduction to ROS 2

Robot Operating System 2 (ROS 2) is a flexible framework for writing robot applications...
```

### Chapter 2: Python-ROS Integration
Add content to `docs/module-1-ros2/chapter-2-python-ros-integration.md`:

```markdown
---
sidebar_position: 2
---

# Chapter 2: Python-ROS Integration

## Using rclpy

rclpy is the Python client library for ROS 2...
```

### Chapter 3: URDF Modeling
Add content to `docs/module-1-ros2/chapter-3-urdf-modeling.md`:

```markdown
---
sidebar_position: 3
---

# Chapter 3: URDF Modeling

## Understanding URDF

Unified Robot Description Format (URDF) is an XML format used to model robot kinematics and dynamics...
```

## Building for Production

To build the static files for deployment:

```bash
npm run build
```

The output will be in the `build/` directory and can be deployed to any static hosting service.

## Deploying to GitHub Pages

### 1. Configure GitHub Pages
Update `docusaurus.config.js` with your GitHub Pages settings:

```javascript
module.exports = {
  // ...
  organizationName: 'your-github-username', // Usually your GitHub org/user name
  projectName: 'your-repo-name', // Usually your repo name
  deploymentBranch: 'gh-pages',
  // ...
};
```

### 2. Deploy
```bash
GIT_USER=<Your GitHub username> npm run deploy
```

This will push the built site to the `gh-pages` branch and make it available at `https://<your-github-username>.github.io/<your-repo-name>/`.

## Next Steps

1. Begin writing content for each chapter following the structure outlined in the specification
2. Add code examples, diagrams, and exercises as needed
3. Ensure all content meets the readability and accuracy standards from the project constitution
4. Test the site regularly during development