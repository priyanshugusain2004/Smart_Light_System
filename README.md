
# 🧠 Smart Light System using Hand Gestures and Human Presence Detection

This Python project uses **MediaPipe**, **OpenCV**, and **Tkinter** to create an intelligent smart light system that:

- Detects **human presence** using pose detection.
- Detects **hand gestures** (raised fingers) to control the **intensity of a smart bulb**.
- Provides a **GUI-based bulb visualization** in real-time.

---

## 🔧 Features

- 🧍 **Automatic On/Off**: The light turns on when a person is detected and turns off when they leave the frame.
- ✋ **Gesture-Based Intensity Control**:
  - 1 finger: Low
  - 2 fingers: Mid
  - 3 fingers: High
  - 4 fingers: Highest
- 🖼️ **Live camera feed** with pose and hand landmark drawing.
- 💡 GUI interface with a colored bulb showing the current light state.

---

## 📦 Requirements

Install the following dependencies **inside a virtual environment** (`.venv`) or globally:

```bash
pip install opencv-python mediapipe
```

Additionally, install **Tkinter** if it's not already installed:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-tk
```

---

## 🚀 How to Run the Project

### 1. Clone or Download the Project

```bash
git clone <your-repo-url> smart_light_system
cd smart_light_system
```

### 2. Create and Activate Virtual Environment (Optional but Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install opencv-python mediapipe
```

And if not already installed:

```bash
sudo apt install python3-tk
```

### 4. Run the Script

```bash
python main.py
```

---

## 🖥️ Application Overview

### 🎥 Camera Input:
- Uses your webcam to continuously read frames.
- Flips the camera feed to act like a mirror.

### 🧍 Human Detection:
- Uses **MediaPipe Pose** to detect a person in the frame.
- When a human is detected, the system assumes someone is present and turns the light to "Low".

### ✋ Gesture Recognition:
- Uses **MediaPipe Hands** to detect how many fingers are raised.
- Maps number of raised fingers to light intensity:
  - 1 finger → Low
  - 2 fingers → Mid
  - 3 fingers → High
  - 4 fingers → Highest

### 💡 GUI Bulb Display:
- Built with **Tkinter**.
- Shows a large bulb with different fill colors based on the light intensity:
  - Gray = Off
  - Cream = Low
  - Yellow = Mid
  - Orange = High
  - Red = Highest

---

## 🛑 Exit the App

- Press **`q`** on the camera window to safely stop the application.

---

## 📷 Troubleshooting

- **No webcam feed?**
  - Ensure your camera is not being used by another application.
  - Try changing the index in `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)`.

- **Getting `ModuleNotFoundError: tkinter`?**
  - Run: `sudo apt install python3-tk`

- **Feedback manager or EGL Warnings?**
  - These are internal library logs. Safe to ignore unless the app crashes.

---

## 📁 File Structure

```
smart_light_system/
├── main.py         # Main Python script
├── README.md       # Project documentation
└── .venv/          # (Optional) Virtual environment
```

---

## 👨‍💻 Author

**Priyanshu Gusain**  
Feel free to modify or extend this project for learning or personal use!
