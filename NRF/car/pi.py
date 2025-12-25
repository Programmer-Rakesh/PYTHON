from RF24 import RF24, RF24_1MBPS, RF24_PA_LOW
import sys, tty, termios, time, struct

radio = RF24(16, 0)  
address = b"CAR01"

radio.begin()
radio.setChannel(108)
radio.setPALevel(RF24_PA_LOW)
radio.setDataRate(RF24_1MBPS)
radio.setPayloadSize(4)
radio.openWritingPipe(address)
radio.setAutoAck(False)
radio.stopListening()

print("NRF connected: True")
print("W/A/S/D = move | SPACE = stop | Q = quit")

def getKey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

try:
    while True:
        key = getKey()

        x, y = 0, 0

        if key == 'w': y = 100
        elif key == 's': y = -100
        elif key == 'a': x = -100
        elif key == 'd': x = 100
        elif key == ' ': x, y = 0, 0
        elif key == 'q': break

        payload = struct.pack('<hh', x, y)
        radio.write(payload)
        print(f"Sent: X={x}, Y={y}")
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    payload = struct.pack('<hh', 0, 0)
    radio.write(payload)