### ---------------------------------------------------------
### Summary: Detect where is the circle.
### Input:  Video / Webcam
### Output: XY of the center & image of the circle(s)
### Nov 11, 2019
### ---------------------------------------------------------
import cv2
import numpy as np
import sys

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)


#print('Number of cameras detected: %d' % num_cameras)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
count = 500
max_x = 500
max_y = 500
max_r = 500
while(True):
    # print("GO")
    ret, gray = cap.read()
    gray = cv2.medianBlur(cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY),5)    #Take in video
    scale_percent = 20 # percent of original size
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.resize(gray, dim, interpolation = cv2.INTER_LANCZOS4)
    # gray = cv2.GaussianBlur(gray, (15,15), 0)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 50)  #Currently only csv.HOUGH_GRADIENT for circle
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
        if max_x != 500 and count > 1:
            if max_x < 150:
                print("DROP " + str(max_x) + ", "+ str(max_y))
            cv2.circle(gray, (max_x,max_y), max_r, (0,255,0),4)
            cv2.rectangle(gray, (max_x-5, max_y-5), (max_x+5, max_y+5), (0, 128, 255), -1)
            max_x = 500
            max_y = 500
            max_r = 500
            count = 500

    cv2.imshow('video',gray)
    if cv2.waitKey(1)==27:# esc Key
        break
cap.release()
cv2.destroyAllWindows()
