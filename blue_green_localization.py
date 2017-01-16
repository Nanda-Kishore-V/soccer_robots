#import cv
import cv2
import numpy as np
import math
import time
#import socket

#TCP_IP = '192.168.43.130'
#TCP_PORT = 8080
#BUFFER_SIZE = 1024

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((TCP_IP, TCP_PORT))
#s.listen(1)

#conn, addr = s.accept()
#print 'Connection address:', addr

WIDTH  = 1100
HEIGHT = 620

cap = cv2.VideoCapture(1)
cap.set(3,1920) #3 - WIDTH
cap.set(4,1080)  #4 - HEIGHT
#img = cv2.imread('',0)
#cv2.imshow("Image",img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cX = 0; cY = 0; yawAngle = 0; yY = 0; yX = 0;
while(True):
    flag = 0
    ret, image = cap.read()

    # height, width = image.shape[:2]
    # res = cv2.resize(image,(int(0.5*width), int(0.5*height)), interpolation = cv2.INTER_CUBIC)

    # cv2.imshow("Original_resized",res)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    flag = 1
    #    break

    pts1 = np.float32([[224,0],[1776,110],[1772,954],[204,1058]])
    pts2 = np.float32([[0,0],[WIDTH,0],[WIDTH,HEIGHT],[0,HEIGHT]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    img = cv2.warpPerspective(image,M,(WIDTH,HEIGHT))

    # cv2.imshow("Perspective",img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    flag = 1
    #    break

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(imgGray,65,255,cv2.THRESH_BINARY)

    # cv2.imshow("Thresh",thresh)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     flag = 1
    #     break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    _,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 2)

    positions = list()
    j = 0
    for i in range(len(contours)):
        c = contours[i]
        area = cv2.contourArea(c)
        if(area > 500 and area < 5000):
            j += 1
            # print "Area" , area
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue
            # cv2.drawContours(img, [c], -1, (0, 255, 0), 2)

            cnt = contours[hierarchy[0][i][2]]
            areaSmall = cv2.contourArea(cnt)
            # print "Area small", areaSmall
            Msmall = cv2.moments(cnt)
            if Msmall["m00"] == 0:
                continue
            yX = int(Msmall["m10"] / Msmall["m00"])
            yY = int(Msmall["m01"] / Msmall["m00"])
            # cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)

            # cv2.imshow("Image",img)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     flag = 1
            #     break

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            yawAngle = math.atan2(cY-yY,cX-yX)*180/math.pi

            position = dict()
            position.update({"bot":j,"cX":cX, "cY":cY, "theta":yawAngle, "yX":yX, "yY":yY})

            positions.append(position)

    color_pstns = list()

    lower_blue = np.array([93,150,130])
    upper_blue = np.array([100,190,155])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(img,img, mask= mask_blue)
    _,contours_blue,hierarchy = cv2.findContours(mask_blue, cv2.RETR_TREE, 2)

    if len(contours_blue) > 0:
        b = contours_blue[0]
        M_blue = cv2.moments(b)
        color_pstn = dict()
        if M_blue["m00"] != 0:
            cX_blue = int(M_blue["m10"] / M_blue["m00"])
            cY_blue = int(M_blue["m01"] / M_blue["m00"])
            color_pstn.update({"color":"blue", "yX":cX_blue, "yY":cY_blue})
        else:
            color_pstn.update({"color":"blue", "yX":-1, "yY":-1})
        color_pstns.append(color_pstn)


    lower_green = np.array([45,110,130])
    upper_green = np.array([53,140,150])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    res_green = cv2.bitwise_and(img,img, mask= mask_green)
    _,contours_green,hierarchy = cv2.findContours(mask_green, cv2.RETR_TREE, 2)
    if len(contours_green) > 0 :
        g = contours_green[0]
        M_green = cv2.moments(g)
        color_pstn = dict()
        if M_green["m00"] != 0:
            cX_green = int(M_green["m10"] / M_green["m00"])
            cY_green = int(M_green["m01"] / M_green["m00"])
            color_pstn.update({"color":"green", "yX":cX_green, "yY":cY_green})
        else:
            color_pstn.update({"color":"green", "yX":-1, "yY":-1})
        color_pstns.append(color_pstn)

    # print "Number of contours: ",j
    if flag == 1:
        break

    for position in positions:
        string = "Bot number: " + str(position["bot"]) + " "
        string += "cX: " + str(position["cX"]) + " cY: " + str(position["cY"]) + " Yaw: " + str(position["theta"]) + " yX: " + str(position["yX"]) + " yY: " + str(position["yY"])
        print string
        print '\n'

    for color_pstn in color_pstns:
        string = "Bot color: " + str(color_pstn["color"]) + " "
        string += "yX: " + str(color_pstn["yX"]) + " yY: " + str(color_pstn["yY"])
        print string
        print '\n'

    time.sleep(0.05);
    #data = conn.recv(BUFFER_SIZE)
    #if not data: continue
    #conn.send(string)
#conn.close()
cap.release()
cv2.destroyAllWindows()
