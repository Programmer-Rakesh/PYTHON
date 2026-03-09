"""
Collect_Training_Data.py
Run this first to record SUM and DOM values while you perform left/right winks.
Press 'l' for left wink, 'r' for right wink, 'n' for no wink (relaxed).
Press 'q' to quit.
"""

import serial
import csv
import time
import os

# Connect to Arduino
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)  # Wait for Arduino reset

# CSV file setup
filename = 'blink_training_data.csv'
file_exists = os.path.isfile(filename)

with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(['sum', 'dom', 'label'])  # Header

    print("="*50)
    print("BLINK TRAINING DATA COLLECTION")
    print("="*50)
    print("Instructions:")
    print("  When you see a line with SUM and DOM, perform a wink and press:")
    print("    l → LEFT wink")
    print("    r → RIGHT wink")
    print("    n → NO wink (relaxed)")
    print("    q → quit and save")
    print("-"*50)

    sample_count = 0
    while True:
        line = arduino.readline().decode().strip()
        if line.startswith("SUM:"):
            # Parse SUM and DOM
            try:
                parts = line.split(',')
                sum_part = parts[0].split(':')[1]
                dom_part = parts[1].split(':')[1]
                sum_val = float(sum_part)
                dom_val = float(dom_part)
            except:
                continue

            print(f"\nSUM={sum_val:.2f}, DOM={dom_val:.2f}")
            label = input("Label (l/r/n/q): ").strip().lower()

            if label == 'q':
                break
            if label in ['l', 'r', 'n']:
                writer.writerow([sum_val, dom_val, label])
                sample_count += 1
                print(f"✓ Saved ({sample_count} samples)")
            else:
                print("✗ Invalid, sample discarded")

print(f"\nTotal samples saved: {sample_count}")
print(f"Data saved to {filename}")