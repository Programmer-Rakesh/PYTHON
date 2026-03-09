"""
Add_New_Data_to_Existing_Dataset.py
Run this to add more training samples to the existing CSV file.
"""

import serial
import csv
import time
import os

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

filename = 'blink_training_data.csv'
if not os.path.isfile(filename):
    print("No existing dataset found. Please run Collect_Training_Data.py first.")
    exit()

with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    print("="*50)
    print("ADD MORE BLINK DATA")
    print("="*50)
    print("Press:")
    print("  l → LEFT wink")
    print("  r → RIGHT wink")
    print("  n → NO wink")
    print("  q → quit")
    print("-"*50)

    sample_count = 0
    while True:
        line = arduino.readline().decode().strip()
        if line.startswith("SUM:"):
            try:
                parts = line.split(',')
                sum_val = float(parts[0].split(':')[1])
                dom_val = float(parts[1].split(':')[1])
            except:
                continue

            print(f"\nSUM={sum_val:.2f}, DOM={dom_val:.2f}")
            label = input("Label (l/r/n/q): ").strip().lower()

            if label == 'q':
                break
            if label in ['l', 'r', 'n']:
                writer.writerow([sum_val, dom_val, label])
                sample_count += 1
                print(f"✓ Added ({sample_count} new samples)")
            else:
                print("✗ Invalid")

print(f"\nAdded {sample_count} new samples to {filename}")