"""
Run_Real_Time_Control.py
Real-time blink detection using ML model. Sends 'L', 'R', or 'S' to ESP32.
"""

import serial
import joblib
import time
import numpy as np

# Load model
model = joblib.load('blink_model.pkl')
print("Model loaded.")

# Connect to Arduino
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)
print("Connected to Arduino.")

# Connect to ESP32 via UART
esp = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(1)
print("Connected to ESP32.")

# Confidence threshold (tune this)
CONFIDENCE_THRESHOLD = 0.7

# Command mapping
CMD_MAP = {'l': 'L', 'r': 'R', 'n': 'S'}
last_cmd = 'S'

def send_command(cmd):
    global last_cmd
    if cmd != last_cmd:
        esp.write(cmd.encode())
        print(f"\n>>> Sending: {cmd}")
        last_cmd = cmd

print("\nReal-time control started. Press Ctrl+C to exit.\n")

try:
    while True:
        line = arduino.readline().decode().strip()
        if line.startswith("SUM:"):
            # Parse SUM and DOM
            try:
                parts = line.split(',')
                sum_val = float(parts[0].split(':')[1])
                dom_val = float(parts[1].split(':')[1])
            except:
                continue

            # Predict
            features = np.array([[sum_val, dom_val]])
            probs = model.predict_proba(features)[0]
            pred = model.predict(features)[0]
            confidence = max(probs)

            # Display
            print(f"\rSUM={sum_val:6.2f} DOM={dom_val:6.2f} | Pred={pred} | Conf={confidence:.2f}", end='')

            # Only act if confidence is high enough
            if confidence >= CONFIDENCE_THRESHOLD:
                cmd = CMD_MAP.get(pred, 'S')
                send_command(cmd)
            else:
                send_command('S')  # Stop if uncertain

except KeyboardInterrupt:
    print("\n\nStopping...")
    send_command('S')

finally:
    arduino.close()
    esp.close()
    print("Connections closed.")