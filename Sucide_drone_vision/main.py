import cv2
import time
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('yolov8s.pt')

# Load video
# video_path = r'C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Sucide_drone_vision\car1.mp4'
# cap = cv2.VideoCapture(video_path)

video_path = r"C:\Users\rakes\OneDrive\Desktop\Codes\Python\Sucide_drone_vision\car1.mp4"
print("USING VIDEO:", video_path)

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
print("Read first frame:", ret)

if not ret:
    print("FAILED TO READ FRAME. Video path might be wrong inside the script.")
    exit()



# Constants
TARGET_CLASS = 'car'
object_locked = False
target_box = None
font = cv2.FONT_HERSHEY_SIMPLEX
bright_green = (0, 255, 0)

# Frame details
# ret, frame = cap.read()
# h, w = frame.shape[:2]

# First read
ret, frame = cap.read()

if not ret or frame is None:
    print("ERROR: Could not read the first frame. Check the video.")
    exit()

h, w = frame.shape[:2]
center_x, center_y = w // 2, h // 2
frame_count = 0
start_time = time.time()


h, w = frame.shape[:2]

center_x, center_y = w // 2, h // 2
# ret = True
frame_count = 0
start_time = time.time()

while ret:
    ret, frame = cap.read()
    if not ret:
        break

    # FPS calculation
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time if elapsed_time > 0 else 0

    # Resize (optional): to improve far object detection
    frame = cv2.resize(frame, (1280, 720))
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2

    # Run YOLO detection
    results = model(frame)[0]
    count = 0

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        class_name = model.names[int(class_id)]
        if class_name == TARGET_CLASS:
            count += 1
            target_box = (int(x1), int(y1), int(x2), int(y2))
            object_locked = True
            break

    if object_locked and target_box:
        x1, y1, x2, y2 = target_box

        # --- Extract raw region before drawing ---
        raw_frame = frame.copy()

        # Calculate center and crop box
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        box_size = 50  # same as reticle size

        crop_x1 = max(0, cx - box_size)
        crop_y1 = max(0, cy - box_size)
        crop_x2 = min(w, cx + box_size)
        crop_y2 = min(h, cy + box_size)

        # Crop from raw frame (without graphics)
        cropped_region = raw_frame[crop_y1:crop_y2, crop_x1:crop_x2]
        display_region = cv2.resize(cropped_region, (150, 150))

        # Display on left-middle of screen
        top_display_y = h // 2 - 75
        bottom_display_y = h // 2 + 75
        left_display_x = 20
        right_display_x = 170

        # Prevent out-of-bounds overwrite
        if display_region.shape[0] == 150 and display_region.shape[1] == 150:
            frame[top_display_y:bottom_display_y, left_display_x:right_display_x] = display_region


        # Axis lines from center of box
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.line(frame, (cx, 0), (cx, cy - 20), bright_green, 2)
        cv2.line(frame, (cx, cy + 20), (cx, h), bright_green, 2)
        cv2.line(frame, (0, cy), (cx - 20, cy), bright_green, 2)
        cv2.line(frame, (cx + 20, cy), (w, cy), bright_green, 2)

        # Diamond shape (sniper tracker) with small gap
        diamond_size = 10
        cv2.polylines(frame, [np.array([
            (cx, cy - diamond_size),
            (cx + diamond_size, cy),
            (cx, cy + diamond_size),
            (cx - diamond_size, cy)
        ], np.int32)], isClosed=True, color=bright_green, thickness=2)

        # top left
        cv2.putText(frame, f"Target: {class_name}", (10, 30), font, 0.6, bright_green, 2)
        cv2.putText(frame, f"Count: {count}", (10, 55), font, 0.6, bright_green, 2)
        cv2.putText(frame, f"Tracker XY: {cx}, {cy}", (10, 80), font, 0.6, bright_green, 2)
        

        # --- Top Right Info (Real-time and Altitude) ---
        current_time = time.strftime("%H:%M:%S", time.localtime())
        altitude = "345m"  # Placeholder for altitude
        cv2.putText(frame, f"Time: {current_time}", (w - 200, 30), font, 0.6, bright_green, 2)
        cv2.putText(frame, f"Altitude: {altitude}", (w - 200, 55), font, 0.6, bright_green, 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (w - 200, 80), font, 0.6, bright_green, 2)

        # --- Bottom Left Info: Distance from sniper to target ---
        distance = int(np.linalg.norm([cx - center_x, cy - center_y]))
        cv2.line(frame, (center_x, center_y), (cx, cy), (0, 0, 255), 2)  # Red line
        cv2.putText(frame, f"Distance: {distance}px", (10, h - 20), font, 0.6, (0, 0, 255), 2)

        # ---- bottom right ----
        lock_status = "ACTIVE" if object_locked else "LOST"
        zoom_level = "1.0x"  # placeholder
        target_status = "Acquired" if count > 0 else "Searching..."

        cv2.putText(frame, f"Lock: {lock_status}", (w - 180, h - 60), font, 0.6, bright_green, 2)
        cv2.putText(frame, f"Zoom: {zoom_level}", (w - 180, h - 40), font, 0.6, bright_green, 2)
        cv2.putText(frame, f"Target: {target_status}", (w - 180, h - 20), font, 0.6, bright_green, 2)



        # Discontinuous Square around target (reticle-style)
        box_size = 50  # size of the square box around the target
        line_len = 10  # length of each corner line
        gap_from_center = 20  # distance between diamond and square

        top_left = (cx - box_size, cy - box_size)
        top_right = (cx + box_size, cy - box_size)
        bottom_left = (cx - box_size, cy + box_size)
        bottom_right = (cx + box_size, cy + box_size)


        # Top-left corner
        cv2.line(frame, top_left, (top_left[0] + line_len, top_left[1]), bright_green, 2)
        cv2.line(frame, top_left, (top_left[0], top_left[1] + line_len), bright_green, 2)

        # Top-right corner
        cv2.line(frame, top_right, (top_right[0] - line_len, top_right[1]), bright_green, 2)
        cv2.line(frame, top_right, (top_right[0], top_right[1] + line_len), bright_green, 2)

        # Bottom-left corner
        cv2.line(frame, bottom_left, (bottom_left[0] + line_len, bottom_left[1]), bright_green, 2)
        cv2.line(frame, bottom_left, (bottom_left[0], bottom_left[1] - line_len), bright_green, 2)

        # Bottom-right corner
        cv2.line(frame, bottom_right, (bottom_right[0] - line_len, bottom_right[1]), bright_green, 2)
        cv2.line(frame, bottom_right, (bottom_right[0], bottom_right[1] - line_len), bright_green, 2)
        
    # Improved sniper crosshair at center
    dot_radius = 4
    line_length = 30
    gap = 10

    # Dot in the center
    cv2.circle(frame, (center_x, center_y), dot_radius, bright_green, -1)

    # Left line
    cv2.line(frame, (center_x - gap - line_length, center_y), (center_x - gap, center_y), bright_green, 2)

    # Right line
    cv2.line(frame, (center_x + gap, center_y), (center_x + gap + line_length, center_y), bright_green, 2)

    # Bottom line
    cv2.line(frame, (center_x, center_y + gap), (center_x, center_y + gap + line_length), bright_green, 2)

    # Show frame
    cv2.imshow("Sniper Object Tracker", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()



