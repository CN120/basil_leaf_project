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
# from matplotlib import pyplot as plt

########## GLOBALS ##############
DROP_SIGNAL = threading.Event()

LEAF_MUTEX = threading.Lock()
good_leaves = []  #will contain coordinates of good leaves
ser = serial.Serial(timeout=None, port="/dev/ttyTHS1", baudrate=115200)
##################################


### ---------------------------------------------------------
### Summary: Convert pixel spaces to inch spaces
### Input:  pixel number
### Output: inches
### ---------------------------------------------------------
def pixelsToInches(pixel):
    return pixel * (18.6/640)

### ---------------------------------------------------------
### Summary: Convert coordinates of leaf from pixel-space 
###          to motor step-space and add to list
### Input:  N/A
### Output: XY of a leaf for stepper motors
### ---------------------------------------------------------
def addLeaf(pix_x, pix_y):
    pass
    #convert coords
    #possibly sort?
    #Mutex lock
    #add coords to good_leaves[]
    #release mutex

### ---------------------------------------------------------
### Summary: Thead function, find coordinates of leaves in image
### Input:  N/A
### Output: None, adds tuples of new leaf coordinates to a list
### ---------------------------------------------------------
def leafTrack():
    global good_leaves
    cap = cv2.VideoCapture(2)
    print("Press ESC to end program")

    ret, frame = cap.read()
    # original = frame.copy()
    # output = frame.copy()
    sample = np.array(frame)
    gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blurred,50,100)
    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.dilate(canny, kernel, iterations=1)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts)==2 else cnts[1]

    print("Number of leaves: ", len(cnts))
    LEAF_MUTEX.acquire()
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        print("---------------wow a leaf: ", x,y,w,h)
        cv2.rectangle(sample, (x,y), (x+w, y+h), (36,255,12), 2)
        # ROI = original[y:y+h, x:x+w]
        r = 5
        t = 1
        cx = int(w / 2)
        cy = int(h / 2)
        print(pixelsToInches(x+cx),pixelsToInches(y+cy))
        cv2.circle(sample, (x+cx, y+cy), r, (255, 0, 0), thickness=t)
        cv2.imshow("identifiedLeaf", sample)

        # Run extraction and ML
        # should return bool if leaf is good or not good
        good = True
        if(good):
            #insert into goodleaves
            good_leaves.append((cx, cy))
        else:
            pass
            # discardLeaves()
    good_leaves.sort()
    LEAF_MUTEX.release()

        
    while True:
        if cv2.waitKey(1)==27:  # esc key
                break
    cap.release()
    cv2.destroyAllWindows()


### ---------------------------------------------------------
### Summary: OUTDATED_Thead function, find coordinates of leaves in image
###          this function is for a constant video feed
### Input:  N/A
### Output: None, adds tuples of new leaf coordinates to a list
### ---------------------------------------------------------
def OUTDATED_leafTrack():
    # global cx, cy
    # cap = cv2.VideoCapture(2)
    # while(True):
    #     ret, frame = cap.read()
    #     original = frame.copy()

    #     sample = np.array(frame)
    #     gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
    #     blurred = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    #     canny = cv2.Canny(blurred,50,100)
    #     kernel = np.ones((3,3),np.uint8)
    #     dilate = cv2.dilate(canny, kernel, iterations=1)
    #     cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #     cnts = cnts[0] if len(cnts)==2 else cnts[1]
    #     for c in cnts:
    #         # print('wow a leaf')
    #         x,y,w,h = cv2.boundingRect(c)
    #         cv2.rectangle(sample, (x,y), (x+w, y+h), (36,255,12), 2)
    #         ROI = original[y:y+h, x:x+w]
    #         r = 5
    #         t = 1
    #         # Center coordinates inside of whole image(cx, cy)
    #         cx = int(w / 2)
    #         cy = int(h / 2)
    #         # addLeaf()
    #         #
    #         cv2.circle(ROI, (cx, cy), r, (255, 0, 0), thickness=t)
    #         cv2.imshow("identifiedLeaf", ROI)
    #     if cv2.waitKey(1)==27:  # esc key
    #         break
    # cap.release()
    # cv2.destroyAllWindows()

    ########## From read_camera_input_test ###################
    cap = cv2.VideoCapture(2)
    print("Press ESC to end program")

    while(True):
        ret, frame = cap.read()

        original = frame.copy()
        output = frame.copy()

        sample = np.array(frame)
        gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
        canny = cv2.Canny(blurred,50,100)
        kernel = np.ones((3,3),np.uint8)
        dilate = cv2.dilate(canny, kernel, iterations=1)
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts)==2 else cnts[1]
        for c in cnts:
            # print("wow a leaf")
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(sample, (x,y), (x+w, y+h), (36,255,12), 2)
            # ROI = original[y:y+h, x:x+w]
            r = 5
            t = 1
            cx = int(w / 2)
            cy = int(h / 2)
            print(pixelsToInches(x+cx),pixelsToInches(y+cy))
            cv2.circle(sample, (x+cx, y+cy), r, (255, 0, 0), thickness=t)
            cv2.imshow("identifiedLeaf", sample)
        
        # cv2.rectangle(sample, (640,300), (640, 350), (255,255,12), 2)
        # cv2.rectangle(sample, (0,300), (0, 350), (255,255,12), 2)
        cv2.imshow("identifiedLeaf", sample)
        #cv2.imshow("croppedimg", croppedimg)
        #cv2.imwrite("croppedimg.png", croppedimg)

        #cv2.imshow('video', output)
        #cv2.imwrite("screen.png", output)
        #break
        if cv2.waitKey(1)==27:  # esc key
            break

    cap.release()
    cv2.destroyAllWindows()



### ---------------------------------------------------------
### Summary: Thead function, tracks when cans are in position to drop leaf
### Input:  N/A
### Output: None, Sets should_drop flag
### Restraints: Clean backgrounf, noisy background will affect HoughCircles performance
### ---------------------------------------------------------
def canTrack():
    limit = 600
    threshold = 50
    cap = cv2.VideoCapture(2)      #Get the last inserted camera
    max_x = limit
    max_y = limit
    max_r = limit
    while(True):
        ret, output = cap.read()
        output = output[150:350]
        # gray = cv2.medianBlur(cv2.cvtColor(output, cv2.COLOR_BGR2GRAY),5)    #Take in video
        #HoughCircles can't take high resoultion images
        #need to use blur to lower the resolution 
        gray = cv2.GaussianBlur(cv2.cvtColor(output, cv2.COLOR_BGR2GRAY), (5,5), 0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 50)  #Currently only csv.HOUGH_GRADIENT for circle
        #ensure at least some circles were found
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x,y,r) in circles: #Find the circules
                #Need to set the x threshold (ORIGINAL: )
                #Offset will be # (need to be added to the last outputs)
                if x > threshold and x != max_x:# and y > 0 and y < 400: #only want circles in certain areas
                    max_x = x
                    max_y = y
                    max_r = r
            #only output if there is circles and we scanned multiple times
            if max_x != limit:
                if max_x < threshold+100:
                    print("DROP " + str(max_x) + ", "+ str(max_y))  #For debugging
                    DROP_SIGNAL.set()   #Signal to main thread that can is in drop position
                    max_x = limit
                    max_y = limit
                    max_r = limit
                else:
                    DROP_SIGNAL.clear() #Clears the drop signal that was set above
                cv2.circle(gray, (max_x,max_y), max_r, (0,255,0),4)
                cv2.rectangle(gray, (max_x-5, max_y-5), (max_x+5, max_y+5), (0, 128, 255), -1)
        else:
            max_x = limit
            max_y = limit
            max_r = limit

        cv2.imshow('video',gray)   #if we want to see the output
        if cv2.waitKey(1)==27:# esc Key
            break
    cap.release()
    cv2.destroyAllWindows()



### ---------------------------------------------------------
### Summary: (Will) pop coordinates of next available leaf
### Input:  N/A
### Output: XY of a leaf for stepper motors
### ---------------------------------------------------------
def getLeaf():
    return (random.randint(0,780),random.randint(0,780))
    # future code below
    # -------------------
    # try:
    #     return good_leaves.pop(0)
    # except:
    #     pass
    #     #leaf list empty, raise warning!
    #     #Signal for new leaves




### ---------------------------------------------------------
### Summary: serves as mainloop control/communication funciton
### Input:  NA
### Output: NA
### ---------------------------------------------------------
def mainLoop():
    print("Listening on Serial Port")
    ENC = 'utf-8'   #serial byte encoding spec
    #variables for storing read, write serial strings
    in_message = None
    out_message = None

    #the try statement allows for graceful shuttdown using ^c (ctrl-c)
    try:
        while True:
            if ser.in_waiting>0:
                in_message = (ser.readline())[:-1]  #reads in message droping '\n'
                
                #decide type of message recieved
                if in_message == b'coords?':
                    out_message = f'{getLeaf()}\n'
                    ser.write(bytes(out_message,ENC))
                elif in_message == b'time?':
                    # waitForCan()
                    DROP_SIGNAL.wait()  # wait indefinately for drop signal
                    ser.write(bytes("drop\n",ENC))
                    print("drop signal sent")
                else:
                    ser.write(bytes("unknown command\n",ENC))
    except KeyboardInterrupt:
        print('\nkeyboard interupt -- Closing Serial Connection')



#                  _          __                  _   _             
#                 (_)        / _|                | | (_)            
#  _ __ ___   __ _ _ _ __   | |_ _   _ _ __   ___| |_ _  ___  _ __  
# | '_ ` _ \ / _` | | '_ \  |  _| | | | '_ \ / __| __| |/ _ \| '_ \ 
# | | | | | | (_| | | | | | | | | |_| | | | | (__| |_| | (_) | | | |
# |_| |_| |_|\__,_|_|_| |_| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|
                                                                  
if __name__ == '__main__':

    #start can_tracking thread
    # can_tracking = threading.Thread(target=canTrack)
    # can_tracking.daemon = True
    # can_tracking.start()

    
    leaf_tracking = threading.Thread(target=leafTrack)
    leaf_tracking.daemon = True
    leaf_tracking.start()

    #consumes any extraneus data in serial bufer
    if ser.in_waiting:
        ser.read(ser.in_waiting)

    mainLoop()    #main/serial communication function
                    #this will act as the main control function for
                    #the Jetson side of things
