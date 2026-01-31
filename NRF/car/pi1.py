from RF24 import RF24, RF24_1MBPS, RF24_PA_LOW
import sys, tty, termios, time, struct

radio = RF24(16, 0)
address = b"CAR01"

radio.begin()
radio.setChannel(108)
radio.setPALevel(RF24_PA_LOW)
radio.setDataRate(RF24_1MBPS)
radio.enableDynamicPayloads()
radio.openWritingPipe(address)
radio.setAutoAck(False)
radio.stopListening()

print("Simple control test - W/S/A/D/Q")

def getKey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

while True:
    key = getKey().lower()
    
    x, y = 0, 0
    if key == 'w': y = 100
    elif key == 's': y = -100
    elif key == 'a': x = -100
    elif key == 'd': x = 100
    elif key == 'q': break
    
    payload = struct.pack('<hh', x, y)
    radio.write(payload)
    print(f"Sent: X={x}, Y={y}")
    time.sleep(0.05)