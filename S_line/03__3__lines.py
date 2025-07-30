# import cv2
# import numpy as np

# # Load Haar face cascade
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # Open webcam
# cap = cv2.VideoCapture(0)

# def draw_semicircle(frame, pt1, pt2, color, thickness=2):
#     mid_x = (pt1[0] + pt2[0]) // 2
#     mid_y = min(pt1[1], pt2[1]) - 100  # Controls how high the arc is
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

#     faces = face_cascade.detectMultiScale(gray, 1.1, 5)
#     face_tops = []

#     for (x, y, w, h) in faces:
#         top_center = (x + w // 2, y)
#         face_tops.append(top_center)

#     if len(face_tops) == 1:
#         pt = face_tops[0]
#         # 🔴 Middle: straight up
#         cv2.line(frame, pt, (pt[0], 0), (0, 0, 255), 2)

#         # 🔴 Left semicircle arc
#         left_target = (pt[0] - 70, 0)
#         draw_semicircle(frame, pt, left_target, (0, 0, 255), 2)

#         # 🔴 Right semicircle arc
#         right_target = (pt[0] + 70, 0)
#         draw_semicircle(frame, pt, right_target, (0, 0, 255), 2)

#     elif len(face_tops) > 1:
#         # Semicircle connections between faces
#         for i in range(len(face_tops)):
#             for j in range(i + 1, len(face_tops)):
#                 draw_semicircle(frame, face_tops[i], face_tops[j], (0, 0, 255), 2)

#     cv2.imshow("Face Connection Tracker", frame)

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

# Get screen resolution
screen_width = 1920  # You can also use pyautogui.size() if needed
screen_height = 1080

def draw_semicircle(frame, pt1, pt2, color, thickness=2):
    mid_x = (pt1[0] + pt2[0]) // 2
    mid_y = min(pt1[1], pt2[1]) - 100
    curve = []
    for t in np.linspace(0, 1, 50):
        x = int((1 - t)**2 * pt1[0] + 2 * (1 - t) * t * mid_x + t**2 * pt2[0])
        y = int((1 - t)**2 * pt1[1] + 2 * (1 - t) * t * mid_y + t**2 * pt2[1])
        curve.append((x, y))
    for i in range(len(curve) - 1):
        cv2.line(frame, curve[i], curve[i + 1], color, thickness)

# Make window fullscreen
cv2.namedWindow("Face Connection Tracker", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Face Connection Tracker", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (screen_width, screen_height))  # Resize to full screen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    face_tops = []

    for (x, y, w, h) in faces:
        top_center = (x + w // 2, y)
        face_tops.append(top_center)

    if len(face_tops) == 1:
        pt = face_tops[0]
        # Straight up
        cv2.line(frame, pt, (pt[0], 0), (0, 0, 255), 2)

        # Left arc
        left_target = (pt[0] - 70, 0)
        draw_semicircle(frame, pt, left_target, (0, 0, 255), 2)

        # Right arc
        right_target = (pt[0] + 70, 0)
        draw_semicircle(frame, pt, right_target, (0, 0, 255), 2)

    elif len(face_tops) > 1:
        for i in range(len(face_tops)):
            for j in range(i + 1, len(face_tops)):
                draw_semicircle(frame, face_tops[i], face_tops[j], (0, 0, 255), 2)

    cv2.imshow("Face Connection Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
