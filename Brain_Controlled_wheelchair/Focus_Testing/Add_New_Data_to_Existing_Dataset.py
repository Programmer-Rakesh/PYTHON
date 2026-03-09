"""
collect_more_data.py - Run this to add more training samples
"""

import serial
import csv
import os
import time

# Check if existing data file exists
file_exists = os.path.isfile('training_data.csv')

# Open file in append mode ('a' instead of 'w')
with open('training_data.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    
    # Write header only if file is new
    if not file_exists:
        writer.writerow(['betaL', 'betaR', 'alphaL', 'alphaR', 'label'])
    
    # Connect to Arduino
    arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    time.sleep(2)
    
    print("="*50)
    print("ADD MORE TRAINING DATA")
    print("="*50)
    print(f"Existing data: {'FOUND' if file_exists else 'NEW FILE'}")
    print("\nPress keys to add labels:")
    print("  r → RELAXED")
    print("  v → VISUAL FOCUS") 
    print("  m → MOTOR FOCUS")
    print("  q → quit and save")
    print("-"*50)
    
    sample_count = 0
    while True:
        line = arduino.readline().decode().strip()
        if line.startswith('FEAT:'):
            parts = line[5:].split(',')
            if len(parts) == 4:
                betaL, betaR, alphaL, alphaR = map(float, parts)
                
                print(f"\nFeatures: {betaL:.1f}, {betaR:.1f}, {alphaL:.1f}, {alphaR:.1f}")
                label = input("Label (r/v/m/q): ").strip().lower()
                
                if label == 'q':
                    break
                if label in ['r','v','m']:
                    writer.writerow([betaL, betaR, alphaL, alphaR, label])
                    sample_count += 1
                    print(f"✓ Saved ({sample_count} new samples)")
    
    print(f"\nAdded {sample_count} new samples to training_data.csv")