import os

import cv2

img = cv2.imread(os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\08__Threshold", 'B1.jpg'))
resized_img = cv2.resize(img, (640, 480))

img_gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(img_gray, 80, 225, cv2.THRESH_BINARY)

thresh = cv2.blur(thresh, (10, 10))
ret, thresh = cv2.threshold(thresh, 80, 255, cv2.THRESH_BINARY)

cv2.imshow('resized_img', resized_img)
cv2.imshow('img_gray', img_gray)
cv2.imshow('thresh', thresh)

cv2.waitKey(0)