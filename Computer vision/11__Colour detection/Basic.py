import cv2
import numpy as np
from PIL import Image
from util import get_limits

yellow = np.array([0, 255, 255])

cap = cv2.VideoCapture(0)



while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        continue

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow)

    cv2.imshow('Original', frame)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    cv2.imshow('frame', mask)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
