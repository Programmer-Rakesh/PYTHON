from ultralytics import  YOLO
import  cv2

# Load yolov8 model
model = YOLO('yolov8n.pt')

# load value
# video_path = r'C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Yolov8 Models\01__Object Tracking\Dog.mp4'
# cap = cv2.VideoCapture(video_path)

cap = cv2.VideoCapture(0) 

# read frame
while True:
    ret, frame = cap.read()
    if not ret:
        break

# detect objects
# track objects
    results = model.track(frame, persist=True)

# plot results
    frame_ = results[0].plot()

#visualize
    cv2.imshow('frame', frame_)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()