import serial
import time
import random
import threading
ser = serial.Serial(timeout=None, port="/dev/ttyTHS1", baudrate=115200)
# s = serial.Serial(timeout=1, port="/dev/ttyTHS2", baudrate=115200)


if ser.in_waiting:
    ser.read(ser.in_waiting)

def calcCoordinates():
    return (random.randint(0,780),random.randint(0,780))

def waitForCan():
    time.sleep(random.randint(1,4))

def main():
    print("Listening")
    ENC = 'utf-8'   #serial byte encoding spec
    in_message = None
    out_message = None
    try:
        while True:
            if ser.in_waiting>0:
                in_message = (ser.readline())[:-1]
                if in_message == b'coords?':
                    out_message = f'{calcCoordinates()}\n'
                    ser.write(bytes(out_message,ENC))
                elif in_message == b'time?':
                    waitForCan()
                    ser.write(bytes("drop\n",ENC))
                    print("now")
                else:
                    ser.write(bytes("unknown command\n",ENC))
    except KeyboardInterrupt:
        print('\nkeyboard interupt -- stopping server')


main()