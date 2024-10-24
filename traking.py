import cv2
import numpy as np

# Load the pre-trained MobileNet SSD model and class labels
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Initialize the tracker
tracker = cv2.TrackerCSRT_create()  # You can use KCF, CSRT, MedianFlow, etc.
initBB = None
frame_count = 0  # To limit detection to every 10 frames

# Start video capture (webcam)
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to improve processing speed
    frame = cv2.resize(frame, (600, 400))
    (h, w) = frame.shape[:2]

    if frame_count % 10 == 0 or initBB is None:
        # Create a blob from the frame
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # Reset tracker
        initBB = None

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                label = CLASSES[idx]

                # Get bounding box coordinates
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Draw bounding box and label
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                text = f"{label}: {confidence:.2f}"
                cv2.putText(frame, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Initialize tracker with detected object
                initBB = (startX, startY, endX - startX, endY - startY)
                tracker.init(frame, initBB)
                break

    # If we have initialized tracking, update the tracker
    if initBB is not None:
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = f"Tracking {label}"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Show the resulting frame
    cv2.imshow('Live Camera Feed', frame)

    # Increment frame counter and check for 'q' to exit
    frame_count += 1
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
