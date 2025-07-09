
# Smart Light System using Hand Gestures and Human Presence Detection

This Python project integrates **MediaPipe**, **OpenCV**, and **Tkinter** to create an intelligent light control system that detects human presence and uses hand gestures to control the brightness of a virtual smart bulb.

It provides real-time webcam input processing and a GUI-based visualization of the bulb’s state and intensity.

---

## Features

- **Automatic On/Off Control**  
  The light turns on when a human is detected in the frame and turns off automatically when the person leaves.

- **Gesture-Based Intensity Adjustment**  
  The system recognizes hand gestures to set brightness levels:
  - 1 finger: Low
  - 2 fingers: Medium
  - 3 fingers: High
  - 4 fingers: Maximum

- **Real-Time Webcam Feed**  
  Displays a live video feed with pose and hand landmark annotations.

- **Interactive Bulb Display**  
  A Tkinter-based interface displays a digital bulb that changes color based on the current intensity level.

---

## Requirements

Ensure you have Python installed, then install the required packages using pip:

```bash
pip install opencv-python mediapipe
```

Install **Tkinter** if not already installed:

**For Ubuntu/Debian-based systems:**

```bash
sudo apt update
sudo apt install python3-tk
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/priyanshugusain2004/Smart_Light_System.git
cd Smart_Light_System
```

### 2. (Optional) Set Up a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install opencv-python mediapipe
```

If needed:

```bash
sudo apt install python3-tk
```

### 4. Run the Application

```bash
python main.py
```

---

## How It Works

### Camera Input  
Uses your webcam to capture video in real-time and flips it to behave like a mirror.

### Human Detection  
Leverages MediaPipe Pose to detect human presence. When a person enters the frame, the light automatically turns on at low intensity.

### Gesture Recognition  
Uses MediaPipe Hands to detect raised fingers. Based on the number of fingers shown, the light intensity changes as follows:
- 1 finger → Low (Cream)
- 2 fingers → Medium (Yellow)
- 3 fingers → High (Orange)
- 4 fingers → Maximum (Red)

If no hand or person is detected, the bulb turns off (Gray).

### GUI Bulb Display  
A simple Tkinter interface shows a color-changing bulb that visually represents the light’s current intensity level.

---

## Exiting the Application

Press `q` in the camera window to exit the program safely.

---

## Troubleshooting

- **Camera feed not showing?**  
  Ensure the camera isn't being used by another application. Try switching the camera index:
  ```python
  cv2.VideoCapture(0) → cv2.VideoCapture(1)
  ```

- **Getting a `tkinter` module error?**  
  Install Tkinter using your package manager:
  ```bash
  sudo apt install python3-tk
  ```

- **Seeing EGL or feedback warnings?**  
  These are internal logs and can typically be ignored unless they cause the application to crash.

---

## File Structure

```
Smart_Light_System/
├── main.py         # Main application script
├── README.md       # Documentation file
└── .venv/          # Optional: Virtual environment folder
```

---

## Author

**Priyanshu Gusain**  
A BCA student exploring real-world applications of computer vision and AI in interactive systems.  
Feel free to fork or contribute to this project. It’s built for experimentation and learning.
