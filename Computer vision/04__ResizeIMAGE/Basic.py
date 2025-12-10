import os
import  cv2

# Declaring path of the image
image_path = os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\04__ResizeIMAGE", 'b4.jpg')

# Reading image
img = cv2.imread(image_path)

# Resizing the image
resized_img = cv2.resize(img, (640, 480))

# For printing the size of the image
print(resized_img.shape)

# Showing image
cv2.imshow('resized_img', resized_img)

cv2.waitKey(0)