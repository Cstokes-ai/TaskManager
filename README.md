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
- `TaskMain.py`: Initializes the main application and manages navigation.
- `MainWindow.py`: Opens the main window with a welcome screen, providing a start to the application.
- `Homepage.py`: Opens the application's dashboard. provides a simple graphical overview of what's expected in the application.
- `CPU.py`: Gathers information from the system. System information includes CPU, Memory, and system storage.
- `Process.py`: Gathers information about processes. Gives the user the ability to shut down individual processes.
- `Scheduling.py`: Opens a scheduling page detailing the scheduling algorithm used, which processes are currently running/stopped, their priority, and which ones use the most space.
- `Graphy.py:


## Installation
### Prerequisites
Ensure you have Python installed (>=3.8). Install required dependencies:
```bash
pip install tk psutil matplotlib
```

### Running the Application
Run the main application using:
```bash
python TaskMain.py
```
#To build the application, use:
pyinstaller --onefile --windowed TaskMain.py


## Usage
1. Launch the application.
2. Navigate using the sidebar to monitor CPU, memory, and processes.
3. Use the refresh button to update metrics.
4. Search or terminate processes as needed.

## License
This project is for personal or internal use only and is open source.


