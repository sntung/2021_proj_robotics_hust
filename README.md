# Control Application for Robotic Arm

A full-stack desktop application for controlling the movements of an industrial welding robot, developed as a graduation research project at Hanoi University of Science and Technology (Feb 2021 – Jun 2021).

## Overview

This project delivers an end-to-end control system for an industrial welding robotic arm, running on Windows. It was built by a 3-person team over 5 months, including kinematics/dynamics computation, real-time PLC communication and operator-facing GUI.

The system computes required motor rotations for desired arm movements, transmits control data to a Programmable Logic Controller (PLC) over Ethernet, and provides a graphical interface for real-time operation and monitoring — achieving target positioning within a 5% margin of error with zero system failures during operation.

## Features

- **Movement calculation** — computes motor rotations for desired end-effector movements using inverse kinematics, validated with zero error against MATLAB-based Kinematics and Dynamics simulations
- **PLC connectivity** — Ethernet-based communication between the application and the robot's PLC, with zero communication interruptions during operation
- **Real-time GUI** — multiple widgets for live operator control and monitoring of robot movement
- **Unified control system** — all modules integrated into a single deployed application for real-time operation

<!--
## Architecture

The application is organized into three core modules:

| Module | Description | Key Libraries |
|---|---|---|
| Movement Calculation | Computes motor rotations from desired movements | NumPy, SciPy |
| Connection | Ethernet communication between app and PLC | Snap7 |
| GUI | Real-time control and monitoring interface | PyQt5 (Qt Widgets) |
-->

## Tech Stack

- **Language:** Python
- **GUI Framework:** Qt Framework (Qt Widgets) via PyQt5
- **Numerical Computing:** NumPy, SymPy
- **Industrial Communication:** Snap7 (PLC Ethernet protocol)
- **Validation:** MATLAB (Kinematics and Dynamics simulation)
- **OS:** Windows

## Getting Started

### Prerequisites

- Python 3.9
- PLC connected via Ethernet (configured with the robot controller)
- Dependencies listed in `requirements.txt` (NumPy, SymPy, PyQt5, python-snap7)

### Installation

```bash
git clone https://github.com/sntung/2021_proj_robotics_hust.git
cd 2021_proj_robotics_hust
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

On launch, the GUI allows the operator to set target positions for the robotic arm. The Movement Calculation module computes the required motor rotations, and the Connection module transmits these to the PLC in real time, with live status shown in the GUI.

## Results

- Motor rotation calculations validated with **zero error** against MATLAB Kinematics/Dynamics simulations
- **Zero communication interruptions** during PLC data transmission
- **Zero critical defects** in the GUI during operation
- Robot consistently reached target positions within a **5% margin of error**
- **Zero system failures** during real-time deployment

## Team

Developed by a 3-person team as a graduation research project at Hanoi University of Science and Technology, with the author leading the project across the full development lifecycle.

## License

Academic project — no license specified. Feel free to reach out if you'd like to use or reference this work.
