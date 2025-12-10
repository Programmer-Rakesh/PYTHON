import os
import  cv2

# Construct the full path to the image
image_path = os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\01__ReadIMAGE", 'b4.jpg')

# Read image
img = cv2.imread(image_path)

# Write image
output_path = os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\01__ReadIMAGE", 'b4_out.jpg')
cv2.imwrite(output_path, img)

# Size of Image
img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_AREA)
#visualise image

# Visualize image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
