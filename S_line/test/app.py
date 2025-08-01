from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(frame):
    img_np = np.frombuffer(base64.b64decode(frame.split(',')[1]), dtype=np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    _, buffer = cv2.imencode('.jpg', img)
    result_frame = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{result_frame}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json['frame']
    result = detect_faces(data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
