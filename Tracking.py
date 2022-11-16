from utilis import *
import cv2

w,h = 360,240
pid = [0.1,0.1,0]
pError = 0
myDrone = initializeTello()
startCounter = 0

while True:

    if startCounter == 0:
        myDrone.takeoff()
        myDrone.move_up(50)
        startCounter = 1
    img = telloGetFrame(myDrone,w,h)
    img,info = findFace(img)
    pError = trackFace(myDrone,info,w,pid,pError)
    #cv2.imshow('test', cv2.cvtColor(img,cv2.COLOR_BGR2HSV))
    print(info[0][0])
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break