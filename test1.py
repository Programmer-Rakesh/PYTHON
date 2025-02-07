import cv2

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

# Focal length estimation (adjust based on real-life testing)
KNOWN_WIDTH = 15  # Assume average face width in cm
FOCAL_LENGTH = 500  # Adjust based on calibration

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale (required for face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Estimate distance (Z-axis) using the formula: Distance = (Known Width * Focal Length) / Perceived Width
        distance = (KNOWN_WIDTH * FOCAL_LENGTH) / w  

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Calculate X and Y coordinates (relative to center of the frame)
        center_x = x + w // 2
        center_y = y + h // 2

        # Display distance and X/Y coordinates on the screen
        text = f"Distance: {int(distance)} cm | X: {center_x} | Y: {center_y}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show the output
    cv2.imshow("Face Detection with Distance & Coordinates", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
