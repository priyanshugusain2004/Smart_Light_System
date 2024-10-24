import tkinter as tk
import os
import cv2
import numpy as np
from threading import Thread

# Initialize the camera and object detection model
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

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
        cap = cv2.VideoCapture(1)  # Use camera 0
        frame_count = 0
        detection_interval = 10  # Process detection every 10th frame

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame for faster processing
            frame = cv2.resize(frame, (1000, 800))
            (h, w) = frame.shape[:2]

            # Process every 10th frame for object detection to reduce lag
            if frame_count % detection_interval == 0:
                # Create a blob from the frame and pass it through the network
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
                net.setInput(blob)
                detections = net.forward()

                person_detected = False

                # Loop over the detections
                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence > 0.5:
                        idx = int(detections[0, 0, i, 1])
                        label = CLASSES[idx]

                        # If a person is detected
                        if label == "person":
                            person_detected = True
                            break

                # Toggle the bulb based on whether a person was detected
                self.toggle_bulb(person_detected)

            # Show the live camera feed in a separate window (optional)
            cv2.imshow('Camera', frame)

            # Update frame counter
            frame_count += 1

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
