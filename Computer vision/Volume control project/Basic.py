import cv2
import  time
import  numpy as np

##############################
wCam, hCam = 1280, 720
##############################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, wCam)
pTime = 0

# Reduce exposure to fix brightness
cap.set(cv2.CAP_PROP_EXPOSURE, 0.1)

while True:
    ret, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime  = cTime

    cv2.putText(img,f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                3, (255, 0, 255), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)