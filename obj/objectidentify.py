import tensorflow as tf
import cv2
import numpy as np

# Load the pre-trained TensorFlow model (SSD MobileNet v2 for example)
detection_model = tf.saved_model.load("ssd_mobilenet_v2/saved_model")

# Load COCO label map (optional)
category_index = {1: "person", 2: "bicycle", 3: "car", 4: "motorbike", 5: "aeroplane", 6: "bus", 7: "train", 8: "truck", 
                  9: "boat", 10: "traffic light", 11: "fire hydrant", 12: "stop sign", 13: "parking meter", 14: "bench",
                  15: "bird", 16: "cat", 17: "dog", 18: "horse", 19: "sheep", 20: "cow", 21: "elephant", 22: "bear", 
                  23: "zebra", 24: "giraffe", 25: "backpack", 26: "umbrella", 27: "handbag", 28: "tie", 29: "suitcase", 
                  30: "frisbee", 31: "skis", 32: "snowboard", 33: "sports ball", 34: "kite", 35: "baseball bat", 
                  36: "baseball glove", 37: "skateboard", 38: "surfboard", 39: "tennis racket", 40: "bottle", 
                  41: "wine glass", 42: "cup", 43: "fork", 44: "knife", 45: "spoon", 46: "bowl", 47: "banana", 48: "apple", 
                  49: "sandwich", 50: "orange", 51: "broccoli", 52: "carrot", 53: "hot dog", 54: "pizza", 55: "donut", 
                  56: "cake", 57: "chair", 58: "sofa", 59: "potted plant", 60: "bed", 61: "dining table", 62: "toilet", 
                  63: "TV monitor", 64: "laptop", 65: "mouse", 66: "remote", 67: "keyboard", 68: "cell phone", 
                  69: "microwave", 70: "oven", 71: "toaster", 72: "sink", 73: "refrigerator", 74: "book", 75: "clock", 
                  76: "vase", 77: "scissors", 78: "teddy bear", 79: "hair drier", 80: "toothbrush"}

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare the frame as input for the model
    input_tensor = tf.convert_to_tensor(frame)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Perform object detection
    detections = detection_model(input_tensor)

    # Process the detection output
    for i in range(int(detections['num_detections'])):
        score = detections['detection_scores'][0][i].numpy()
        if score > 0.5:  # Filter by confidence threshold
            class_id = int(detections['detection_classes'][0][i].numpy())
            box = detections['detection_boxes'][0][i].numpy()

            # Get bounding box coordinates and draw on the frame
            h, w, _ = frame.shape
            y1, x1, y2, x2 = int(box[0] * h), int(box[1] * w), int(box[2] * h), int(box[3] * w)
            label = category_index[class_id] if class_id in category_index else "Unknown"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label}: {score:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the output frame
    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
