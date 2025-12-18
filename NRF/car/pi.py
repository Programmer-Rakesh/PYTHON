from RF24 import RF24
import sys, tty, termios, time, struct

radio = RF24(16, 0)  # ✅ Keeping your working pins
address = b"CAR01"

radio.begin()
radio.setChannel(108)
radio.setPayloadSize(4)  # ✅ FIXED: 2 shorts = 4 bytes
radio.openWritingPipe(address)
radio.stopListening()

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
        elif key == 'q':
            break

        # Pack as 2 signed shorts (int16_t), each 2 bytes = 4 bytes total
        payload = struct.pack('<hh', x//100, y//100)
        
        success = radio.write(payload)
        
        if success:
            print(f"Sent: X={x//100}, Y={y//100}")
        else:
            print("Send failed!")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Send stop command before exit
    payload = struct.pack('<hh', 0, 0)
    radio.write(payload)