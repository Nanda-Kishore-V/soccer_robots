import cv2
import numpy as np
import math
import time
WIDTH  = 1100
HEIGHT = 620
FPS = 28
LENGTH = 375 #cm
BREADTH = 215 #cm

cap = cv2.VideoCapture(1)
cap.set(3,1920) #3 - WIDTH
cap.set(4,1080)  #4 - HEIGHT
#img = cv2.imread('',0)
#cv2.imshow("Image",img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cX = 0; cY = 0; yawAngle = 0; yY = 0; yX = 0;cX_ball_old=0 ; cY_ball_old=0; cX_ball = 0;cY_ball = 0;
while(True):
    flag = 0
    ret, image = cap.read()

    # height, width = image.shape[:2]
    # res = cv2.resize(image,(int(0.5*width), int(0.5*height)), interpolation = cv2.INTER_CUBIC)

    # cv2.imshow("Original_resized",res)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    flag = 1
    #    break

    pts1 = np.float32([[38,0],[1758,82],[1732,1022],[20,1044]])
    pts2 = np.float32([[0,0],[WIDTH,0],[WIDTH,HEIGHT],[0,HEIGHT]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    img = cv2.warpPerspective(image,M,(WIDTH,HEIGHT))

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(imgGray,65,255,cv2.THRESH_BINARY)


    #
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_ball = np.array([27,110,130])
    upper_ball = np.array([34,175,190])

    mask_ball = cv2.inRange(hsv, lower_ball, upper_ball)
    res_ball = cv2.bitwise_and(img,img, mask= mask_ball)

    # cv2.imshow("Ball",mask_ball)
    # if cv2.waitKey(1) == 0xFF & ord('q'):
    #     flag = 1
    #     break
    contours_ball,hierarchy = cv2.findContours(mask_ball, cv2.RETR_TREE, 2)
    # print "Image Shape :" , img.shape

    if len(contours_ball) > 0:
        b = contours_ball[0]
        M_ball = cv2.moments(b)
        if M_ball["m00"] != 0:
            cX_ball = int(M_ball["m10"] / M_ball["m00"])
            cY_ball = int(M_ball["m01"] / M_ball["m00"])
            # print "CX : " , cX_ball , " Cy : " , cY_ball
        else:
            cX_ball = cX_ball_old
            cY_ball = cY_ball_old
    vX_ball_pixel = (cX_ball - cX_ball_old) * FPS
    vY_ball_pixel = (cY_ball - cY_ball_old) * FPS
    vX_ball = (cX_ball - cX_ball_old)*LENGTH*FPS/WIDTH
    vY_ball = (cY_ball - cY_ball_old)*BREADTH*FPS/HEIGHT
    #print vY_ball_pixel#,vY_ball
    cX_predict_1 = cX_ball + vX_ball_pixel
    cY_predict_1 = cY_ball + vY_ball_pixel
    cv2.line(img,(cX_ball,cY_ball),(cX_predict_1,cY_predict_1) ,(255,255,0),5)
    cv2.line(img,(100,0),(100,1022),(255,0,0),5)
    cv2.line(img,(1000,0),(1000,1022),(255,0,0),5)
    if(vX_ball_pixel<0):
        dest_X = 100
    else:
        dest_X = 1000
    if cv2.waitKey(1) & 0xFF == ord('q'):
       flag = 1
       break
    if(vX_ball_pixel):
        time = ((dest_X - cX_ball)/(vX_ball_pixel*1.0))
        #print (cX_ball - dest_X)
        #print time
        print cY_ball," cY ",time," t ",vY_ball_pixel, " vY"
        dest_Y = cY_ball + int(time * vY_ball_pixel)
        print dest_Y
        cv2.circle(img,(dest_X,dest_Y), 5, (0,0,255), -1)
    cv2.imshow("Perspective",img)
    cX_ball_old = cX_ball
    cY_ball_old = cY_ball
#     # time.sleep(0.05);
#     #data = conn.recv(BUFFER_SIZE)
#     #if not data: continue
#     #conn.send(string)

# #conn.close()
cap.release()
cv2.destroyAllWindows()
# Create a black image
