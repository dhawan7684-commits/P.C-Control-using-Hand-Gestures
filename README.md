# AI Hand Gesture Controller

## Overview

This project is a real-time computer vision system that utilizes a **Convolutional Neural Network (CNN)** to control Windows, Mac, or Linux system functions through hand landmarks. The system features a **Transit Buffer** logic designed to prevent accidental command triggers when the user is transitioning between different hand gestures.

## Gesture and Action Map

The system is calibrated to recognize 10 distinct hand orientations, each mapped to a specific operating system command.

| Label | Gesture | Action Triggered | Logic Type |
| --- | --- | --- | --- |
| 0 | Fist | Idle (Transit Buffer) | Neutral |
| 1 | Open Palm | Take Screenshot | Action |
| 2 | Index Finger | Open Start Menu | Action |
| 3 | Middle Finger | Scroll Down | Continuous |
| 4 | Pinky Finger | Scroll Up | Continuous |
| 5 | Victory Sign | Volume Up | Action |
| 6 | Rock Sign | Volume Down | Action |
| 7 | Thumbs Up | Open Settings | Action |
| 8 | L-Shape (Thumb/Index) | Open Google Chrome | Multi-Step |
| 9 | Pinky + Thumb | Minimize All Windows | Action |

## Technical Requirements

To ensure the system functions without module resolution errors, the following dependencies must be installed:

* **TensorFlow**: 2.12.0
* **MediaPipe**: 0.10.0
* **Protobuf**: version less than 4.0.0
* **NumPy**: version less than 2.0.0
* **PyAutoGUI**: Latest stable version

## Setup and Troubleshooting

Based on current development logs, please ensure the following configurations are met:

1. **Module Imports**: Ensure `import time` is declared at the top of `main_control.py` to avoid "time is not defined" errors during action execution.
2. **Interpreter Selection**: If using Visual Studio Code, ensure the Python Interpreter is set to the local virtual environment (venv) to resolve "Pylance" missing module warnings.
3. **Execution**: The "Fist" gesture (Label 0) should be held momentarily when moving between active gestures to reset the trigger state.
