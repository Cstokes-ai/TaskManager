# System Tracker & Task Manager

## Overview
This project is a Python-based system tracker and task manager with a graphical user interface (GUI) built using Tkinter. It allows users to monitor CPU and memory usage, view process activity, manage process scheduling, and terminate processes as needed. The application follows object-oriented programming (OOP) principles and is structured across multiple files for modularity.

## Features
- **User Authentication**: Login system for access control.
- **Real-Time Monitoring**:
  - CPU usage tracking
  - Memory usage tracking
- **Process Management**:
  - View running processes
  - Search for specific processes
  - Terminate selected processes
- **Process Scheduling Overview**: Displays scheduling details.
- **Graphical Data Representation**: Uses Matplotlib for trend visualization.
- **Navigation Panel**: Provides quick access to different sections.

## File Structure
- `main.py`: Initializes the main application and manages navigation.
- `navigation.py`: Handles the sidebar for switching between different pages.
- `pages.py`: Contains different UI sections (CPU, Memory, Process, Scheduling, Home).
- `graph.py`: Implements real-time data visualization.
- `auth.py`: Manages user login and authentication.

## Installation
### Prerequisites
Ensure you have Python installed (>=3.8). Install required dependencies:
```bash
pip install tk psutil matplotlib
```

### Running the Application
Run the main application using:
```bash
python main.py
```

## Usage
1. Launch the application.
2. Log in using your credentials.
3. Navigate using the sidebar to monitor CPU, memory, and processes.
4. Use the refresh button to update metrics.
5. Search or terminate processes as needed.

## License
This project is for personal or internal use only and is open source.


