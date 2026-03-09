"""
CODE 3: realtime_control.py
Run this for actual car control after model is trained
"""

import serial
import joblib
import time
import threading
from collections import deque
import numpy as np

# Load the trained model
print("Loading ML model...")
model = joblib.load('focus_model.pkl')
print("✓ Model loaded")

# Connect to Arduino via USB
print("Connecting to Arduino...")
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)
print("✓ Connected to Arduino")

# Connect to ESP32 via UART
print("Connecting to ESP32...")
esp = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(1)
print("✓ Connected to ESP32")

# State tracking
last_command = 'S'  # Start with STOP
current_state = 0    # 0=relaxed, 1=visual, 2=motor
state_names = ['RELAXED', 'VISUAL FOCUS', 'MOTOR FOCUS']

# Smoothing buffer (optional)
feature_buffer = deque(maxlen=3)

def send_command(cmd):
    """Send a single character command to ESP32"""
    global last_command
    if cmd != last_command:
        esp.write(cmd.encode())
        command_names = {'F': 'FORWARD', 'L': 'LEFT', 'R': 'RIGHT', 'S': 'STOP'}
        print(f"\n>>> SENDING: {command_names.get(cmd, cmd)} ({cmd})")
        last_command = cmd

def handle_blink(direction):
    """Handle blink detection - overrides focus"""
    print(f"\n!!! BLINK DETECTED: {direction}")
    if direction == 'LEFT':
        send_command('L')
    else:  # RIGHT
        send_command('R')

print("\n" + "="*50)
print("REAL-TIME CONTROL ACTIVE")
print("="*50)
print("\nCommands will be sent to ESP32:")
print("  F = FORWARD (when in MOTOR FOCUS state)")
print("  L = LEFT (when blink detected)")
print("  R = RIGHT (when blink detected)")
print("  S = STOP")
print("\nPress Ctrl+C to exit")
print("-"*50)

try:
    while True:
        # Read from Arduino
        line = arduino.readline().decode().strip()
        
        if not line:
            continue
            
        if line.startswith('>>> BLINK:'):
            # Blink detected - immediate action
            direction = line.split()[-1]
            handle_blink(direction)
            
        elif line.startswith('FEAT:'):
            # Features received - run ML prediction
            parts = line[5:].split(',')
            if len(parts) == 4:
                betaL, betaR, alphaL, alphaR = map(float, parts)
                
                # Optional: Add to buffer for smoothing
                feature_buffer.append([betaL, betaR, alphaL, alphaR])
                
                # Use average of last few readings for stability
                if len(feature_buffer) >= 2:
                    features = np.mean(feature_buffer, axis=0).reshape(1, -1)
                else:
                    features = np.array([[betaL, betaR, alphaL, alphaR]])
                
                # Predict mental state
                state = model.predict(features)[0]
                current_state = state
                
                # Get prediction probabilities (confidence)
                probs = model.predict_proba(features)[0]
                confidence = max(probs) * 100
                
                # Display current status
                print(f"\rState: {state_names[state]:12} | "
                      f"Confidence: {confidence:.1f}% | "
                      f"βL:{betaL:5.1f} βR:{betaR:5.1f} αL:{alphaL:5.1f} αR:{alphaR:5.1f}", 
                      end='', flush=True)
                
                # Send command based on state
                if state == 2:  # MOTOR FOCUS
                    send_command('F')
                else:  # RELAXED or VISUAL FOCUS
                    send_command('S')
                    
except KeyboardInterrupt:
    print("\n\nStopping...")
    send_command('S')  # Send STOP before exiting
    
finally:
    arduino.close()
    esp.close()
    print("Connections closed")