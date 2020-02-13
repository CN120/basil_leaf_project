#For Communication
import serial
import time
import random
import threading

#for Can Tracking
import cv2
import numpy as np
import sys

#For Leaf Tracking
from matplotlib import pyplot as plt

DROP_MUTEX = threading.Lock()
should_drop = 0

LEAF_MUTEX = threading.Lock()


ser = serial.Serial(timeout=None, port="/dev/ttyTHS1", baudrate=115200)

def leafTrack():
    global cx, cy
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        original = frame.copy()

        sample = np.array(frame)
        gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
        canny = cv2.Canny(blurred,50,100)
        kernel = np.ones((3,3),np.uint8)
        dilate = cv2.dilate(canny, kernel, iterations=1)
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts)==2 else cnts[1]
        for c in cnts:
            print('wow a leaf')
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(sample, (x,y), (x+w, y+h), (36,255,12), 2)
            ROI = original[y:y+h, x:x+w]
            r = 5
            t = 1
            # Center coordinates (cx, cy)
            cx = int(w / 2)
            cy = int(h / 2)
            #
            #cv2.circle(ROI, (cx, cy), r, (255, 0, 0), thickness=t)
            #cv2.imshow("identifiedLeaf", ROI)
        if cv2.waitKey(1)==27:  # esc key
            break
    cap.release()
    cv2.destroyAllWindows()

def canTrack():
    global should_drop
    cap = cv2.VideoCapture(0)
    count = 500
    max_x = 500
    max_y = 500
    max_r = 500
    while(True):
        ret, frame = cap.read()
        output = frame.copy()
        cv2.imshow('video',output)
        gray = cv2.medianBlur(cv2.cvtColor(output, cv2.COLOR_BGR2GRAY),5)    #Take in video
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 50)  #Currently only csv.HOUGH_GRADIENT for circle
        #ensure at least some circles were found
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            count += 1
            for (x,y,r) in circles: #FInd the circules
                #Need to set the x threshold (ORIGINAL: )
                #Offset will be # (need to be added to the last outputs)
                if x > 50 and x < max_x and y > 150 and y < 300: #only want circles in certain areas
                    max_x = x
                    max_y = y
                    max_r = r
            #only output if there is circles and we scanned multiple times
            if max_x != 500 and count > 2:
                DROP_MUTEX.acquire()
                if max_x < 150:
                    # print("DROP " + str(max_x) + ", "+ str(max_y))
                    should_drop = 1         ###MUTE
                else:
                    should_drop = 0
                DROP_MUTEX.release()
                cv2.circle(gray, (max_x,max_y), max_r, (0,255,0),4)
                cv2.rectangle(gray, (max_x-5, max_y-5), (max_x+5, max_y+5), (0, 128, 255), -1)
                max_x = 500
                max_y = 500
                max_r = 500
                count = 500

        # cv2.imshow('video',gray)   #if we want to see the output
        if cv2.waitKey(1)==27:# esc Key
            break
    cap.release()
    cv2.destroyAllWindows()



def calcCoordinates():
    return (random.randint(0,780),random.randint(0,780))

def waitForCan():
    global should_drop
    while True:
        DROP_MUTEX.acquire()
        if should_drop==1:
            should_drop = 0
            DROP_MUTEX.release()
            return
        DROP_MUTEX.release()

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






can_tracking = threading.Thread(target=canTrack)
can_tracking.daemon = True
can_tracking.start()


# s = serial.Serial(timeout=1, port="/dev/ttyTHS2", baudrate=115200)

if ser.in_waiting:
    ser.read(ser.in_waiting)

main()