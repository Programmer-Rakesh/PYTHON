import os
import  cv2

img = cv2.imread(os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\10__Drawing", 'white.jpg'))

print(img.shape)

# line
cv2.line(img,(100, 150), (300, 450),(0, 255, 0), 3)

# rectangle


# circle

# text

cv2.imshow('img', img)
cv2.waitKey(0)