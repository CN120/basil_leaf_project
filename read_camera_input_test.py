### ------------------------
### Summary: Use the RealSense Camera to identify center of leaves
### Input: RealSense Depth Camera
### Output: XY of the center & image of the leaf
### Author: Sherene (sevictor@)
### Notes: Needs white background 
### ------------------------

import numpy as np
import cv2
#import pyrealsense2 as rs
from matplotlib import pyplot as plt

# If VideoCapture and frame.copy fail, try unplugging and replugging the camera
cap = cv2.VideoCapture(-1)
print("Press ESC to end program")

while(True):
    ret, frame = cap.read()
    #print("ret: ", ret)
    #print("frame: ", frame)
    original = frame.copy()
    output = frame.copy()

    # GRABCUT METHOD - didn't work, not fast enough for video
    #mask = np.zeros(output.shape[:2], np.uint8)
    #bgdModel = np.zeros((1, 65), np.float64)
    #fgdModel = np.zeros((1, 65), np.float64)
    # Modify rect based on the size of your cropped/extracted image
    #rect = (50, 50, 450, 290)
    # rect is only used when mode==GC_INIT_WITH_RECT
    #cv2.grabCut(output, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    #mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    #croppedimg = frame*mask2[:,:,np.newaxis]

    # SIFT METHOD - circuitdigest.com/tutorial 
    # "Real Life Object Detection Using OpenCV Python Detecting Objects in Live Video
    # STOPPED because working on development from Jupyter notebook demo
    #height, width = frame.shape[:2]
    #top_left_x = int(width / 3) 
    #top_left_y = int((height / 2) + (height / 4))
    #bottom_right_x = int((width / 3) * 2)
    #bottom_right_y = int((height / 2) - (height / 4))
    #print("height: ", height)
    #print("width: ", width)
    #cv2.rectangle(frame, )

    # MY METHOD - based on Jupyter notebook demo (see team documentation)
    #
    sample = np.array(frame)
    gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    canny = cv2.Canny(blurred,50,100)
    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.dilate(canny, kernel, iterations=1)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts)==2 else cnts[1]
    for c in cnts:
        print("wow a leaf")
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(sample, (x,y), (x+w, y+h), (36,255,12), 2)
        # ROI = original[y:y+h, x:x+w]
        r = 5
        t = 1
        cx = int(w / 2)
        cy = int(h / 2)
        print(cx,cy)
        cv2.circle(sample, (x+cx, y+cy), r, (255, 0, 0), thickness=t)
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


