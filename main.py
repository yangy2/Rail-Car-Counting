#RAILCAR COUNTER
#by Yilin Yang

import numpy as np
import cv2
import csv
import queue
import time

### INSERT VIDEO FILENAME HERE ###
input_path = 'TrainingData.mp4'

#Counter Variables
left = 0
right = 0

#Video Setup
cap = cv2.VideoCapture(input_path) 
bgs = cv2.createBackgroundSubtractorMOG2()
fourccc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.mp4', fourccc, 20.0, (640, 480))

#Get Video Dimensions
width = cap.get(3)
height = cap.get(4)
imgsize = width*height

#Create Line Demarcation
leftline = int(1*(width/5))
rightline = int(4*(width/5))
horizon = int(height/3)

#Left Boundary
pt1 = [leftline, 0]
pt2 = [leftline, horizon]
pts_L1 = np.array([pt1, pt2], np.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))

#Right Boundary
pt3 = [rightline, 0];
pt4 = [rightline, horizon];
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

#Horizontal Boundary
pt5 = [0, horizon]
pt6 = [width, horizon]
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))

font = cv2.FONT_HERSHEY_SIMPLEX

#Image Morphing Parameters
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)) 
threshold = 2000 #minimum size to recognize unique contour

#Begin Procedure
start = time.time()

#Write log to external csv file
with open('output_log.csv', 'w', newline='') as csvfile:
    fieldnames = ['car_id', 'entry_point', 'entry_time', 'exit_point', 'exit_time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#Open video file
while(cap.isOpened()):
    ret, frame = cap.read() #read frame
    mask = bgs.apply(frame, None, -1) #apply BGS to frame

    #Apply image morphing to BGS frame...
    try:
        ret, binary = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY) #remove noise
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel) #image opening
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel) #image closing
        binary = cv2.dilate(binary, kernel, iterations = 7) #brighten
    #... As long as there are frames to process
    except:
        print('LEFT: ' + str(left))
        print('RIGHT: ' + str(right))
        print('TOTAL: ' + str(left+right))
        print('The End')
        break

    _, contour, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_NONE)
    #Find Image Contours
    for i in contour:
        area = cv2.contourArea(i)
        if area > threshold:
            M = cv2.moments(i)
            #identify center of contour
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            #box contour
            x, y, w, h = cv2.boundingRect(i)
            #img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            #Count using Cross Product (Bx-Ax)*(Cy-Ay)-(By-Ay)*(Cx-Ax)
            #(0,horizon) (width,horizon) (cx,cy) Cross Product
            if ((width-0)*(cy-horizon)-(horizon-horizon)*(cx-0)) < 0:
                if cx <= leftline + 1 and cx > leftline: left += 1
                if cx >= rightline - 1 and cx < rightline: right += 1

    #Display data
    string1 = 'LEFT: ' + str(left)
    string2 = 'RIGHT: ' + str(right)
    string3 = 'TOTAL: ' + str(left+right)
    
    string4 = str(int((time.time()-start)/60)) + ':'
    if((time.time()-start)%60<10): string4 = string4 + '0'
    string4 = string4 + str(int((time.time()-start)%60))

    string5 = 'Rutgers Rail Program'
    string6 = 'Yilin Yang'

    string7 = 'Car X' + str(int((time.time()-start)%10)) + ' entered'
    string8 = 'Bottom Left'

    frame = cv2.polylines(frame, [pts_L1], False, (0, 0, 255), thickness=2)
    frame = cv2.polylines(frame, [pts_L2], False, (255, 0, 0), thickness=2)
    frame = cv2.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)

    cv2.putText(frame, string1, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, string1, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.putText(frame, string2, (550, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, string2, (550, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    cv2.putText(frame, string3, (int(width/2-30), 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, string3, (int(width/2-30), 40), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(frame, 'TIME:', (10, 450), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, string4, (10, 470), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(frame, string5, (int(width/3+30), 450), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, string6, (int(width/2-30), 470), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(frame, string7, (510, 450), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, string8, (525, 470), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, 'Placeholder', (530, 430), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    #Display video
    cv2.imshow('Press ESC to close early', frame)
    out.write(frame)

    #Abort procedure if ESC pressed
    if cv2.waitKey(30) & 0xff == 27: break

#End procedure
cap.release()
out.release()
cv2.destroyAllWindows()
