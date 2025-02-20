import serial
import time
import cv2

# Initialize serial communication (Change COM port accordingly)
arduinoData = serial.Serial('COM5', 9600)  
time.sleep(2)  # Allow time for connection

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture (0 = internal webcam, 1 = external)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Constants for distance calculation (Calibrate these values)
KNOWN_WIDTH = 14.0  # Approximate width of a human face in cm
FOCAL_LENGTH = 500.0  # Adjust based on actual camera calibration

def calculate_distance(known_width, focal_length, width_in_frame):
    """Calculate the distance from the camera to the face."""
    if width_in_frame > 0:
        return (known_width * focal_length) / width_in_frame
    return -1  # Invalid width case

def send_distance_to_arduino(distance):
    """Send distance to Arduino via Serial."""
    distance_str = f"{distance:.2f}\r"  # Format distance to 2 decimal places
    arduinoData.write(distance_str.encode())  
    print(f"Distance: {distance:.2f} cm")  # Print for debugging

while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 8, minSize=(120, 120))

    for (x, y, w, h) in faces:
        distance = calculate_distance(KNOWN_WIDTH, FOCAL_LENGTH, w)  # Get distance

        # Draw a red rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Send distance data to Arduino
        send_distance_to_arduino(distance)

    # Display video
    cv2.imshow("Face Tracking", frame)

    # Press 'd' to exit
    if cv2.waitKey(20) & 0xFF == ord('d'):
        break

# Release resources
capture.release()
cv2.destroyAllWindows()
arduinoData.close()
