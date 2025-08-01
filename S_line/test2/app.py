from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run your ML model on img here
    # result = model(img)
    # Let's simulate with dummy response
    result = "Line detected!"  # Replace with real model prediction

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
