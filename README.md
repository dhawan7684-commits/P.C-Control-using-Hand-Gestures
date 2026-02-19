AI Hand Gesture Controller
A real-time computer vision system that uses a **Convolutional Neural Network (CNN)** to control Windows/Mac/Linux functions via hand landmarks. It introduces a **Transit Buffer** logic to prevent accidental triggers while switching between gestures.

Gesture & Action Map

The system maps 10 hand orientations to specific OS commands.

| Label | Gesture               | Action Triggered         | Logic Type   |
| **0** | Fist                  | Idle (Transit Buffer)    | Neutral      |
| **1** | Open Palm             | Take Screenshot          | Action       |
| **2** | Index Finger          | Open Start Menu          | Action       |
| **3** | Middle Finger         | Scroll Down              | Continuous   |
| **4** | Pinky Finger          | Scroll Up                | Continuous   |
| **5** | Victory Sign          | Volume Up                | Action       |
| **6** | Rock Sign             | Volume Down              | Action       |
| **7** | Thumbs Up             | Open Settings            | Action       |
| **8** | L-Shape (Thumb/Index) | Open Google Chrome       | Multi-Step   |
| **9** | Pinky + Thumb         | Minimize All Windows     | Action       |