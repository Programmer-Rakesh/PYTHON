from RF24 import *
import time
import numpy as np
import os

# Use your pins: CE=16, CSN=0 (SPI0 CE0)
radio = RF24(16, 0)

CHANNELS = 80   # NRF24 supports channels 0–79
samples = [0] * CHANNELS

def init_radio():
    if not radio.begin():
        print("NRF24 not detected!")
        exit(1)

    radio.setAutoAck(False)
    radio.setRetries(0, 0)
    radio.setPALevel(RF24_PA_MIN)
    radio.setDataRate(RF24_2MBPS)
    radio.stopListening()

    print("NRF24 ready! Starting spectrum scan...\n")

def scan_channels():
    for ch in range(CHANNELS):
        radio.setChannel(ch)
        radio.startListening()
        time.sleep(0.002)

        # Read RPD (Received Power Detect)
        if radio.testRPD():
            samples[ch] += 1

        radio.stopListening()

def print_graph():
    os.system("clear")
    print("2.4GHz Spectrum Scanner (NRF24)\n")
    print("Channel : Power\n")

    max_val = max(samples) if max(samples) > 0 else 1

    for ch in range(CHANNELS):
        bar = int((samples[ch] / max_val) * 50)
        print(f"{ch:02d} [{'-' * bar}>] {samples[ch]}")

def main():
    init_radio()
    while True:
        scan_channels()
        print_graph()

try:
    main()
except KeyboardInterrupt:
    print("\nStopped.")
