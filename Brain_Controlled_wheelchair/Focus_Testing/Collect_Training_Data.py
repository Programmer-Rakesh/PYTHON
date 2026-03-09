"""
CODE 1: collect_training_data.py
Run this first to record EEG features while you perform different mental tasks
"""

import serial
import csv
import time

# Connect to Arduino via USB
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

# Create CSV file to store training data
with open('training_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['betaL', 'betaR', 'alphaL', 'alphaR', 'label'])
    
    print("=" * 50)
    print("TRAINING DATA COLLECTION")
    print("=" * 50)
    print("\nInstructions:")
    print("  r → Record as RELAXED state (eyes open, blank wall)")
    print("  v → Record as VISUAL FOCUS (look at an object intently)")
    print("  m → Record as MOTOR FOCUS (imagine moving forward)")
    print("  q → Quit and save")
    print("\nWait for features to appear, then press a key to label them")
    print("-" * 50)
    
    while True:
        # Read line from Arduino
        line = arduino.readline().decode().strip()
        
        if line.startswith('FEAT:'):
            # Extract the 4 feature values
            parts = line[5:].split(',')
            if len(parts) == 4:
                betaL, betaR, alphaL, alphaR = map(float, parts)
                
                # Show the features
                print(f"\nFeatures received:")
                print(f"  Beta Left:  {betaL:.2f}%")
                print(f"  Beta Right: {betaR:.2f}%")
                print(f"  Alpha Left: {alphaL:.2f}%")
                print(f"  Alpha Right:{alphaR:.2f}%")
                
                # Ask for label
                label = input("Label this sample (r/v/m): ").strip().lower()
                
                if label == 'q':
                    print("\nSaving and exiting...")
                    break
                    
                if label in ['r', 'v', 'm']:
                    # Save to CSV
                    writer.writerow([betaL, betaR, alphaL, alphaR, label])
                    print(f"✓ Saved as {label}")
                else:
                    print("✗ Invalid key, sample discarded")

print(f"\nTraining data saved to 'training_data.csv'")