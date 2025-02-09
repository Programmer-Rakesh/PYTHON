import cv2
import serial
import time
import numpy as np  # ✅ Finally not forgetting NumPy!

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)  # Change COM port if needed
time.sleep(2)  # Wait for connection

# Load OpenCV face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face():
    cap = cv2.VideoCapture(0)  # Use system camera
    start_time = time.time()
    face_found = False

    while (time.time() - start_time) < 6:  # Search for a face for 6 seconds
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            center_x = x + w // 2
            center_y = y + h // 2

            servo_x = int((center_x / frame.shape[1]) * 180)
            servo_y = int((center_y / frame.shape[0]) * 180)

            arduino.write(f"FACE_X:{servo_x}\n".encode())
            arduino.write(f"FACE_Y:{servo_y}\n".encode())
            face_found = True
        else:
            arduino.write("NO_FACE\n".encode())

    cap.release()
    return face_found

while True:
    arduino.write("CHECK_OBSTACLE\n".encode())  # Ask Arduino if obstacle is detected
    response = arduino.readline().decode().strip()

    if response == "OBSTACLE_DETECTED":
        print("Obstacle detected! Switching to Face Tracking mode.")
        arduino.write("PAUSE_RADAR\n".encode())  # 🚀 Send pause command to Arduino
        face_detected = detect_face()

        if not face_detected:
            print("No face detected. Resuming Radar mode.")
            arduino.write("RESUME_RADAR\n".encode())  # 🚀 Resume radar after 6 sec

    time.sleep(1)  # Wait before checking again
