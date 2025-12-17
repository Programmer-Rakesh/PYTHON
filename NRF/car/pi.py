from RF24 import RF24
import sys, tty, termios, time, struct

radio = RF24(22, 0)
address = b"CAR01"

radio.begin()
radio.setChannel(108)
radio.setPayloadSize(8)     # 👈 VERY IMPORTANT
radio.openWritingPipe(address)
radio.stopListening()

print("W/A/S/D = move | SPACE = stop")

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
    key = getKey()

    x = 0
    y = 0

    if key == 'w':
        y = 10000
    elif key == 's':
        y = -10000
    elif key == 'a':
        x = -10000
    elif key == 'd':
        x = 10000
    elif key == ' ':
        x = 0
        y = 0

    payload = struct.pack('<hh', x//100, y//100)  # 👈 2 SHORTS
    radio.write(payload)

    time.sleep(0.05)
