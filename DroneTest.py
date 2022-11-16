from djitellopy import Tello
import cv2
import time

######################################################################
width = 320
height = 240
startCounter = 1  # 0 FOR FIGHT 1 FOR TESTING
######################################################################

# initialize
flyBoy = Tello()
flyBoy.connect()
flyBoy.for_back_velocity = 0
flyBoy.left_right_velocity = 0
flyBoy.up_down_velocity = 0
flyBoy.yaw_velocity = 0
flyBoy.speed = 0

print(flyBoy.get_battery())

flyBoy.streamoff()
flyBoy.streamon()

while True:

    # getting drone image
    frame_read = flyBoy.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))


    if startCounter == 0:
        flyBoy.takeoff()
        time.sleep(8)
        flyBoy.rotate_clockwise(90)
        time.sleep(3)
        flyBoy.move_left(35)
        time.sleep(3)
        flyBoy.land()
        startCounter = 1

    # sending to drone
    # if flyBoy.send_rc_control:
    #     flyBoy.send_rc_control(flyBoy.left_right_velocity, flyBoy.for_back_velocity, flyBoy.up_down_velocity, flyBoy.yaw_velocity)

    # DISPLAY IMAGE
    cv2.imshow("MyResult", img)

    # Emergency land
    if cv2.waitKey(1) & 0xFF == ord('q'):
        flyBoy.land()
        break