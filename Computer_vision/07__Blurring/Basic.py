import  os

import  cv2
img = cv2.imread(os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\07__Blurring", 'B1.jpg'))
resized_img = cv2.resize(img, (640, 480))

k_size = 7  #larger the number, more the blur
img_blur1 = cv2.blur(resized_img, (k_size, k_size))
img_blur2 = cv2.GaussianBlur(resized_img, (k_size, k_size), 3)
img_blur3 = cv2.medianBlur(resized_img, k_size)   #This can partially change a noised image to a clear image

cv2.imshow('resized_img', resized_img)
cv2.imshow('img_blur1', img_blur1)
cv2.imshow('img_blur2', img_blur2)
cv2.imshow('img_blur3', img_blur3)


cv2.waitKey(0)