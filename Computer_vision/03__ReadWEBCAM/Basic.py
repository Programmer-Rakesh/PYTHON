import cv2

# read webcam
webcam = cv2.VideoCapture(0)

# visualize webcam
while True:
    ret, frame = webcam.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    cv2.imshow('frame', frame)

    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows outside the loop
webcam.release()
cv2.destroyAllWindows()
