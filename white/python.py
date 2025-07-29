from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Load video
video_path = r'C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\white\white.mp4'
cap = cv2.VideoCapture(video_path)

# Original video size
orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Resize scale for output display
scale = 0.8

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    tracked_crop = None

    for result in results.boxes:
        cls = int(result.cls[0])
        if cls == 0:  # 'person'
            x1, y1, x2, y2 = map(int, result.xyxy[0])

            # Add padding to bounding box for better coverage
            padding = 20  # <-- You can edit this padding value
            x1 = max(x1 - padding, 0)
            y1 = max(y1 - padding, 0)
            x2 = min(x2 + padding, frame.shape[1])
            y2 = min(y2 + padding, frame.shape[0])

            area = (x2 - x1) * (y2 - y1)
            crop = frame[y1:y2, x1:x2].copy()

            # Select the largest area person
            if tracked_crop is None or area > tracked_crop[0]:
                tracked_crop = (area, crop)

            # Draw red bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Overlay crop image at top center (adjusted down + portrait style)
    if tracked_crop:
        _, person_crop = tracked_crop

        # Resize crop to portrait video style
        crop_h = 280  # <-- You can edit height here
        crop_w = int(crop_h * 9 / 16)  # Maintain 9:16 aspect ratio

        resized_crop = cv2.resize(person_crop, (crop_w, crop_h))

        # Positioning
        x_offset = (frame.shape[1] - crop_w) // 2
        y_offset = 40  # <-- You can adjust Y-offset (vertical position) here

        frame[y_offset:y_offset + crop_h, x_offset:x_offset + crop_w] = resized_crop

    # Resize output video frame
    output_frame = cv2.resize(frame, (int(orig_width * scale), int(orig_height * scale)))

    cv2.imshow("Result", output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
