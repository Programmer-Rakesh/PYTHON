import os
import  cv2

# Read Video
video_path = os.path.join(r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Computer vision\02__ReadVIDEO", "Vid.mp4")

video = cv2.VideoCapture(video_path)

# Visualize video

ret = True
while ret:
    ret, frame = video.read()

    if ret:
        cv2.imshow('frame', frame)
        cv2.waitKey(35)