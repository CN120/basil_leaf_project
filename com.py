import serial
import time
import random
import threading


#GLOBAL VARIABLES
max_x, max_y = 780,780 #max x and y coordinates of the Gantry system
ENC = 'utf-8'   #encoding to be used over serial



#setup serial port
port = serial.Serial(timeout=None, port="/dev/ttyTHS1", baudrate=115200)   
# s = serial.Serial(timeout=1, port="/dev/ttyTHS2", baudrate=115200)

#clears any data that may be sitting in serial buffer on launch
if port.in_waiting:
    port.read(port.in_waiting)


#this function will eventually return the coordinates of a leaf
#for right now it is a placeholder that returns random coordinates
def calcCoordinates():
    return (random.randint(0,max_x),random.randint(0,max_y))

#this function will eventually calculate time until drop and send drop signal
#for now it waits a few seconds and then send a drop command
def waitForCan():
    time.sleep(random.randint(1,4))
    port.write(bytes("go\n",ENC))


def main():
    print("Serial port open - listening for input") 
    print("Press Ctrl+C to stop program")
    in_message, out_message = None, None    #strings that will hold input and output from serial port
    try:
        while True:
            if port.in_waiting>0:
                in_message = (port.readline())[:-1] #read in message from serial port and drop the \n
                
                if in_message == b'coords?':
                    #send coordinates of next leaf
                    out_message = f'{calcCoordinates()}\n'
                    port.write(bytes(out_message,ENC))
                elif in_message == b'time?':
                    #respond only when leaf should be dropped
                    waitForCan()
                else:
                    port.write(bytes("unknown command\n",ENC))
                    print("Received unknown command")
    except KeyboardInterrupt:
        print('\nkeyboard interupt -- serial port closed')


main()