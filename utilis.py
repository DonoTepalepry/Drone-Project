from djitellopy import Tello
import cv2
import numpy as np


def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def telloGetFrame(myDrone,w=360,h=240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img

def findColor(img):
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 19, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 110, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 240, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 153, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)
    while True:
        img = cv2.imread(path)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,4)

    myFaceListC = []
    myFAceListArea = []

    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = x + w//2
        cy = y+h//2
        area = w*h
        myFAceListArea.append(area)
        myFaceListC.append([cx,cy])

    if len(myFAceListArea) != 0:
        i = myFAceListArea.index(max(myFAceListArea))
        return img, [myFaceListC[i], myFAceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(myDrone,info,w,pid,pError):
    #pid controller
    error = info[0][0] - w//2
    speed = pid[0]*error + pid[1]*(error-pError)
    speed = int(np.clip(speed,-100,100))
    #error = info[0][0] - w//2
    #speedFor = pid[0]*error + pid[1]*(error-pError)
    #speedFor = int(np.clip(speedFor,-100,100)) #test again once i get home speedFor was originally just speed
    print(speed)
    if info[0][0] != 0:
        myDrone.yaw_velocity = speed
        myDrone.for_back_velocity = speed # try changing this to speed instead of speedFor not done yet
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)

    return error