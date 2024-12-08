import cv2
import mediapipe as mp
import tkinter as tk

# Initialize Mediapipe for Hands and Pose
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# States and colors for the bulb
states = ["Off", "Low", "Mid", "High", "Highest"]
colors = {
    "Off": "gray",
    "Low": "#FFFDD0",
    "Mid": "yellow",
    "High": "orange",
    "Highest": "red"
}
state_index = 0  # Start with "Off"
human_detected = False  # Track human presence

# Function to update the bulb state
def update_bulb_state(new_index):
    global state_index
    state_index = new_index
    new_state = states[state_index]
    bulb_canvas.itemconfig(bulb_body, fill=colors[new_state])
    state_label.config(text=new_state)

# Function to count raised fingers
def count_raised_fingers(hand_landmarks):
    fingers = [False] * 5  # Initialize all fingers as not raised

    # Tip and base landmarks for fingers
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    finger_bases = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]

    # Check if each finger is raised
    for i in range(5):
        if i == 0:  # Special case for thumb (horizontal motion)
            fingers[i] = hand_landmarks.landmark[finger_tips[i]].x < hand_landmarks.landmark[finger_bases[i]].x
        else:  # Vertical motion for other fingers
            fingers[i] = hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_bases[i]].y

    return sum(fingers)

# Function to process video frames and detect gestures and human presence
def detect_gestures_and_human_presence():
    global state_index, human_detected
    ret, frame = cap.read()
    if not ret:
        return

    # Flip the frame horizontally for a natural mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect human presence using Pose
    pose_results = pose.process(rgb_frame)
    is_human_now_detected = pose_results.pose_landmarks is not None

    # Handle human detection
    if is_human_now_detected:
        if not human_detected:  # If human is newly detected, turn the bulb On
            human_detected = True
            update_bulb_state(1)  # Turn bulb to "Low" state initially
    else:
        if human_detected:  # If human leaves the frame, turn the bulb Off
            human_detected = False
            update_bulb_state(0)  # Turn Off the bulb

    # If human is detected, detect hand gestures
    if human_detected:
        hand_results = hands.process(rgb_frame)

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Count the number of raised fingers
                raised_fingers = count_raised_fingers(hand_landmarks)

                # Update the bulb state based on the number of raised fingers
                if raised_fingers == 1:
                    update_bulb_state(1)  # Low
                elif raised_fingers == 2:
                    update_bulb_state(2)  # Mid
                elif raised_fingers == 3:
                    update_bulb_state(3)  # High
                elif raised_fingers == 4:
                    update_bulb_state(4)  # Highest

    # Draw pose landmarks (optional)
    if is_human_now_detected and pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Show the frame
    cv2.imshow("Hand Gesture and Human Detection", frame)

    # Close the application if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        root.destroy()
        cap.release()
        cv2.destroyAllWindows()
        return

    # Call the function again
    root.after(10, detect_gestures_and_human_presence)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create the main window
root = tk.Tk()
root.title("Bulb Intensity and Presence Control")
root.geometry("500x600")  # Set a larger window size

# Create a canvas for the bulb
bulb_canvas = tk.Canvas(root, width=400, height=400, bg="white")
bulb_canvas.pack(pady=20)

# Draw the bulb shape
bulb_body = bulb_canvas.create_oval(100, 50, 300, 300, fill="gray")  # Enlarged bulb body
bulb_base = bulb_canvas.create_rectangle(170, 300, 230, 350, fill="black")  # Enlarged bulb base

# Label to show the current state
state_label = tk.Label(root, text="Off", font=("Helvetica", 20))
state_label.pack(pady=10)

# Start detection
root.after(10, detect_gestures_and_human_presence)

# Run the application
root.mainloop()
