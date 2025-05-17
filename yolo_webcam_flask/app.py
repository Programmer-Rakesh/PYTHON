# from flask import Flask, render_template, Response
# from ultralytics import YOLO
# import cv2

# app = Flask(__name__)

# # Load YOLOv8 model
# model = YOLO("yolov8n.pt")

# # Open webcam
# # cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("http://192.168.1.3:4747/video")



# def generate_frames():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         # Run YOLO tracking
#         results = model.track(frame, persist=True)
#         frame_ = results[0].plot()

#         # Encode frame
#         ret, buffer = cv2.imencode(".jpg", frame_)
#         frame_bytes = buffer.tobytes()

#         yield (b"--frame\r\n"
#                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video')
# def video():
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)



# from flask import Flask, Response
# import cv2
# from ultralytics import YOLO

# app = Flask(__name__)

# # Load YOLOv8 model (change to your custom model path if needed)
# model = YOLO("yolov8n.pt")

# # Use the virtual webcam Iriun exposes
# cap = cv2.VideoCapture(0)  # Try 1 if 0 doesn't work

# def gen_frames():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         # Run YOLOv8 inference
#         results = model(frame, imgsz=640)

#         # Draw results on the frame
#         annotated_frame = results[0].plot()

#         # Resize to fit on screen (optional)
#         annotated_frame = cv2.resize(annotated_frame, (640, 480))

#         # Encode to JPEG
#         ret, buffer = cv2.imencode('.jpg', annotated_frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return '''
#     <html>
#     <head><title>Iriun + YOLOv8 Stream</title></head>
#     <body>
#         <h1 style="text-align:center;">YOLOv8 Live Feed from iPhone (Iriun)</h1>
#         <div style="text-align:center;">
#             <img src="/video" width="640" height="480">
#         </div>
#     </body>
#     </html>
#     '''

# @app.route('/video')
# def video():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)



from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLOv8 model (you can use yolov8n.pt, yolov8s.pt, etc.)
model = YOLO('yolov8n.pt')

# Use the correct Iriun camera index (change this after testing)
camera_index = 1  # change to 1 or 2 based on test
cap = cv2.VideoCapture(camera_index)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Run YOLOv8 inference
        results = model(frame, imgsz=640, verbose=False)[0]
        annotated_frame = results.plot()

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h1>YOLOv8 iPhone Camera Live Feed</h1>
        <img src="/video" width="640" height="480">
    </body>
    </html>
    '''

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
