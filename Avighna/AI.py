import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load video
cap = cv2.VideoCapture(r"C:\Users\rakes\OneDrive\Desktop\Codes\Python\Avighna\videoplayback.mp4")

# FPS control
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30
delay = int(1000 / fps)

def region_of_interest(img):
    height, width = img.shape[:2]
    mask = np.zeros_like(img)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width, int(height * 0.6)),
        (0, int(height * 0.6))
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(img, mask)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (520, 700))

    # ================== LANE DETECTION ==================
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 60, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    edges = cv2.Canny(mask, 50, 150)
    roi = region_of_interest(edges)

    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 50,
                            minLineLength=40, maxLineGap=20)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # ================== CENTER + SIDE LINES ==================
    frame_center = frame.shape[1] // 2
    offset = 80

    left_line = frame_center - offset
    right_line = frame_center + offset

    # Default colors
    left_color = (0, 255, 255)   # yellow
    right_color = (0, 255, 255)

    # ================== VEHICLE DETECTION ==================
    results = model(frame, verbose=False)

    vehicle_count = 0
    status = "SAFE"

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])

            if cls in [2, 3, 5, 7]:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                vehicle_count += 1

                # Draw RED box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"V{vehicle_count}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 0, 255), 2)

                # ================= OVERLAP LOGIC =================
                overlaps_left = (x1 <= left_line <= x2)
                overlaps_center = (x1 <= frame_center <= x2)
                overlaps_right = (x1 <= right_line <= x2)

                # Change line color on collision
                if overlaps_left:
                    left_color = (0, 0, 255)   # RED

                if overlaps_right:
                    right_color = (0, 0, 255)  # RED

                # Status logic
                if overlaps_center or (overlaps_left and overlaps_right):
                    status = "SAFE"
                elif overlaps_left or overlaps_right:
                    status = "ALERT"

    # ================== DRAW LINES (THINNER) ==================
    cv2.line(frame, (frame_center, 0), (frame_center, 680), (255, 0, 0), 1)  # blue center
    cv2.line(frame, (left_line, 0), (left_line, 680), left_color, 1)         # left
    cv2.line(frame, (right_line, 0), (right_line, 680), right_color, 1)      # right

    # ================== DISPLAY ==================
    color = (0, 255, 0) if status == "SAFE" else (0, 0, 255)

    cv2.putText(frame, status, (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.putText(frame, f"Vehicles: {vehicle_count}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Lane + Vehicle Detection", frame)

    if cv2.waitKey(delay) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()