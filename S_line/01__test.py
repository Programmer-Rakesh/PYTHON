
# import cv2
# import numpy as np

# # Load face detector
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # Open webcam
# cap = cv2.VideoCapture(0)

# def draw_semicircle(frame, pt1, pt2, color, thickness=2):
#     mid_x = (pt1[0] + pt2[0]) // 2
#     mid_y = min(pt1[1], pt2[1]) - 100
#     curve = []
#     for t in np.linspace(0, 1, 50):
#         x = int((1 - t)**2 * pt1[0] + 2 * (1 - t) * t * mid_x + t**2 * pt2[0])
#         y = int((1 - t)**2 * pt1[1] + 2 * (1 - t) * t * mid_y + t**2 * pt2[1])
#         curve.append((x, y))
#     for i in range(len(curve) - 1):
#         cv2.line(frame, curve[i], curve[i+1], color, thickness)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Face detection
#     faces = face_cascade.detectMultiScale(gray, 1.1, 5)
#     face_top = None
#     if len(faces) > 0:
#         x, y, w, h = faces[0]
#         face_top = (x + w // 2, y)

#     # Black book detection using dark region
#     _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
#     kernel = np.ones((5, 5), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     book_top = None

#     if contours:
#         largest = max(contours, key=cv2.contourArea)
#         area = cv2.contourArea(largest)
#         if area > 2000:
#             x, y, w, h = cv2.boundingRect(largest)
#             book_top = (x + w // 2, y)
#             # Blue rectangle and text removed ✅

#     # Draw red lines / arc
#     if face_top and book_top:
#         draw_semicircle(frame, face_top, book_top, (0, 0, 255), 2)
#     elif face_top:
#         cv2.line(frame, face_top, (face_top[0], 0), (0, 0, 255), 2)
#     elif book_top:
#         cv2.line(frame, book_top, (book_top[0], 0), (0, 0, 255), 2)

#     # Show result
#     cv2.imshow("Face + Book Tracker", frame)
#     # cv2.imshow("Debug Threshold", thresh)  # You can comment this out too if not needed

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()




import cv2
import numpy as np

# Load Haar face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open webcam
cap = cv2.VideoCapture(0)

def draw_semicircle(frame, pt1, pt2, color, thickness=2):
    mid_x = (pt1[0] + pt2[0]) // 2
    mid_y = min(pt1[1], pt2[1]) - 100
    curve = []
    for t in np.linspace(0, 1, 50):
        x = int((1 - t)**2 * pt1[0] + 2 * (1 - t) * t * mid_x + t**2 * pt2[0])
        y = int((1 - t)**2 * pt1[1] + 2 * (1 - t) * t * mid_y + t**2 * pt2[1])
        curve.append((x, y))
    for i in range(len(curve) - 1):
        cv2.line(frame, curve[i], curve[i+1], color, thickness)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Face detection
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    face_top = None
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_top = (x + w // 2, y)

    # Book detection (dark object)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    book_top = None

    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(largest)
            book_top = (x + w // 2, y)

    # 🔴 Fixed red line from face to top (always shown)
    if face_top:
        cv2.line(frame, face_top, (face_top[0], 0), (0, 0, 255), 2)

    # 🔴 Semicircle when both detected
    if face_top and book_top:
        draw_semicircle(frame, face_top, book_top, (0, 0, 255), 2)
    elif book_top:
        # If only book detected, show book's vertical red line
        cv2.line(frame, book_top, (book_top[0], 0), (0, 0, 255), 2)

    # Show final output
    cv2.imshow("Face + Book Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
