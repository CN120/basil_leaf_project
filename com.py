import serial
import time
import random
ser = serial.Serial(timeout=None, port="/dev/ttyTHS1", baudrate=115200)
# s = serial.Serial(timeout=1, port="/dev/ttyTHS2", baudrate=115200)

# try:
#     s.open()
# except:
#     pass
# # s.reset_input_buffer()
# # s.reset_output_buffer()
# send = "hello\r\n"
# s.write(bytes(send, 'utf-8'))
# ret = s.readline()
# print(ret)
# dec = ret.decode('utf-8')
# print(dec)


def calcCoordinates():
    return (random.randint(0,100),random.randint(0,100))

def calcDropTime():
    time.sleep(3.4)

def main():
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
                    calcDropTime()
                    ser.write(bytes("drop\n",ENC))
                else:
                    ser.write(bytes("unknown command\n"),ENC)
    except KeyboardInterrupt:
        print('\nkeyboard interupt -- stopping server')


main()