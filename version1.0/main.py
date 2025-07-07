import tkinter as tk
import os
import cv2
import mediapipe as mp
from threading import Thread

# Initialize MediaPipe solutions
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


class BulbApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulb ON/OFF with Camera Detection")

        # Set the size of the window
        self.root.geometry("450x600")

        # Bulb is initially OFF
        self.bulb_status = False

        # Create the label to show bulb status
        self.label = tk.Label(self.root, text="Bulb is OFF", font=("Arial", 20), fg="red")
        self.label.pack(pady=20)

        # Create a canvas to display the bulb image
        self.canvas = tk.Canvas(self.root, width=200, height=250)
        self.canvas.pack()

        # Load the OFF and ON images
        try:
            self.bulb_off_image = tk.PhotoImage(file=os.path.abspath("finalproject\off.PNG"))
            self.bulb_on_image = tk.PhotoImage(file=os.path.abspath("finalproject\on.PNG"))
        except Exception as e:
            print(f"Error loading images: {e}")
            self.label.config(text="Error: Images not found")
            return

        # Display the initial OFF image
        self.canvas_image = self.canvas.create_image(100, 150, image=self.bulb_off_image)

        # Start camera detection in a separate thread
        self.camera_thread = Thread(target=self.detect_person)
        self.camera_thread.daemon = True
        self.camera_thread.start()

    def toggle_bulb(self, status):
        """Change bulb status based on detection."""
        # Only update the GUI when there's a state change (ON/OFF toggle)
        if status != self.bulb_status:
            self.bulb_status = status
            if status:
                # Bulb is ON
                self.label.config(text="Bulb is ON", fg="green")
                self.canvas.itemconfig(self.canvas_image, image=self.bulb_on_image)
            else:
                # Bulb is OFF
                self.label.config(text="Bulb is OFF", fg="red")
                self.canvas.itemconfig(self.canvas_image, image=self.bulb_off_image)

    def detect_person(self):
        """Detect person using the camera feed and toggle the bulb."""
        cap = cv2.VideoCapture(0)  # Use the default camera
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert the BGR frame to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process the frame with MediaPipe Pose
                results = pose.process(frame_rgb)

                # Check if a pose is detected (presence of a person)
                person_detected = results.pose_landmarks is not None

                # Toggle the bulb based on whether a person was detected
                self.toggle_bulb(person_detected)

                # Draw pose landmarks on the frame
                if person_detected:
                    mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
                    )

                # Show the live camera feed in a separate window (optional)
                cv2.imshow('Camera', frame)

                if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
                    break

        # Release the camera and close windows
        cap.release()
        cv2.destroyAllWindows()


# Create the main window
root = tk.Tk()

# Create the BulbApp object
app = BulbApp(root)

# Start the GUI event loop
root.mainloop()
