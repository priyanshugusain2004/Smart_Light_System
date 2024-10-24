import cv2

# Open the default camera (usually 0)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If frame is read correctly, ret will be True
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # Display the resulting frame
    cv2.imshow('Video Output', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
