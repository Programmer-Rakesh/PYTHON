import os
import  cv2

img = cv2.imread(os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\10__Drawing", 'white.jpg'))

print(img.shape)

# line
cv2.line(img,(100, 150), (300, 450),(0, 255, 0), 3)

# rectangle
cv2.rectangle(img, (200, 350), (450, 600), (0, 0, 255), 10)  # if we put -1 instead of 10, the box will be filled with colour

# circle
cv2.circle(img, (500, 550), 150, (255, 0, 0), 10)

# text
cv2.putText(img, 'Hey you!', (800, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)


cv2.imshow('img', img)
cv2.waitKey(0)