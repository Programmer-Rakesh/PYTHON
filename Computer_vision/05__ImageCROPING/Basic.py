import os
import  cv2

image_path = os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\05__ImageCROPING", 'b4.jpg')

img = cv2.imread(image_path)

# Cropping a resized image
resized_img = cv2.resize(img, (640, 480))
cropped_img = resized_img[320:640, 420:840]

cv2.imshow('cropped_img', cropped_img)
cv2.waitKey(0)