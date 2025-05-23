# from ultralytics import  YOLO
# import  cv2

# # Load yolov8 model
# model = YOLO('yolov8n.pt')

# # load value
# # video_path = r'C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Yolov8 models\01__Object Detection\darjeling.mp4'
# # cap = cv2.VideoCapture(video_path)

# cap = cv2.VideoCapture(0)

# # read frame
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break


# # track objects
#     results = model.track(frame, persist=True)

# # plot results
#     frame_ = results[0].plot()

#     frame_resized = cv2.resize(frame_, (520, 780))

# #visualize
#     cv2.imshow('frame', frame_resized)
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()





from ultralytics import YOLO
import cv2
import torch

# Check and use GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Running on: {device}")

# Load YOLOv8 model
model = YOLO('yolov8n.pt').to(device)

# Load video file
video_path = r'C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Yolov8 models\01__Object Detection\darjeeling.mp4'
cap = cv2.VideoCapture(video_path)

# Frame read loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame before detection for faster inference
    frame_resized = cv2.resize(frame, (500, 780))

    # Run detection (predict is faster than track)
    results = model.predict(frame_resized, conf=0.5, verbose=False, device=device)

    # Plot results on the frame
    plotted_frame = results[0].plot()

    # Optional: Display without further resizing
    cv2.imshow('YOLOv8 Detection', plotted_frame)

    # Exit loop on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
cv2.destroyAllWindows()
