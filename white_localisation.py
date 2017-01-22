import cv2
import numpy as np
import math
import time

WIDTH  = 1100
HEIGHT = 620

cap = cv2.VideoCapture(0)
cap.set(3,1920) #3 - WIDTH
cap.set(4,1080)  #4 - HEIGHT

cX = 0; cY = 0; yawAngle = 0; yY = 0; yX = 0;cX_new = 0;cY_new = 0
while(True):
    flag = 0
    ret, image = cap.read()

    pts1 = np.float32([[224,0],[1776,110],[1772,954],[204,1058]])
    pts2 = np.float32([[0,0],[WIDTH,0],[WIDTH,HEIGHT],[0,HEIGHT]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    img = cv2.warpPerspective(image,M,(WIDTH,HEIGHT))

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(imgGray,65,255,cv2.THRESH_BINARY)

    cv2.imshow("Thresh",thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        flag = 1
        break

    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 2)

    for i in range(len(contours)):
        c = contours[i]
        area = cv2.contourArea(c)
        if(area > 500 and area < 5000):
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            print "cX: ",cX," cY: ",cY

            crop = img[(cY-40):(cY+40),(cX-40):(cX+40)]
            imgwhiteGray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
            ret,thresh_crop = cv2.threshold(imgwhiteGray,65,255,cv2.THRESH_BINARY)

            contours_white,hierarchy_white = cv2.findContours(thresh_crop, cv2.RETR_TREE, 2)

            # print "length: ",len(contours_white)
            for j in range(len(contours_white)):
                c_white = contours_white[j]
                area_white = cv2.contourArea(c_white)
                # print "area_white",area_white
                if(area_white > 1000 and area_white < 4500):
                    M_White = cv2.moments(c_white)
                    if M_White["m00"] == 0:
                        continue
                    cX_new = int(M_White["m10"]/M_White["m00"])
                    cY_new = int(M_White["m01"]/M_White["m00"])

                # cv2.drawContours(crop, [contours_white[j]], -1, (0, 255, 0), 2) #parent - bluish green
                count = 0
                for j in range(len(contours_white)):
                    # print hierarchy_white[0][j][2]
                    if hierarchy_white[0][j][2] == -1: #Assumption: the small white circles doesnt have any children
                        area_small = cv2.contourArea(contours_white[j])
                        count += 1
                        if area_small > 200 and area_small < 350:
                            M_small = cv2.moments(contours_white[j])
                            if M_small["m00"] == 0:
                                continue
                            yX = int(M_small["m10"]/M_small["m00"])
                            yY = int(M_small["m01"]/M_small["m00"])
                    elif hierarchy_white[0][j][3] == 0: #Assumption: the outermost contour is always 0
                        area_black = cv2.contourArea(contours_white[j])
                        M = cv2.moments(contours_white[j])
                        if M["m00"] == 0:
                            continue
                        cX_new = int(M["m10"]/M["m00"])
                        cY_new = int(M["m01"]/M["m00"])
            yawAngle = math.atan2(cY_new-yY,cX_new-yX)*180/math.pi
            print "cX: ",cX," cY: ",cY," cX_new: ",cX_new," cY_new: ",cY_new," yX: ",yX," yY: ",yY," yawAngle: ",yawAngle
            print "Count: ",count

            # cv2.imshow("Image",crop)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     flag = 1
            #     break

#conn.close()
cap.release()
cv2.destroyAllWindows()
