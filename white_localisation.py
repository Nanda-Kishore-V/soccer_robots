import cv2
import numpy as np
import math
import time

WIDTH  = 1100
HEIGHT = 620

cap = cv2.VideoCapture(1)
cap.set(3,1920) #3 - WIDTH
cap.set(4,1080)  #4 - HEIGHT

pts1 = np.float32([[68,42],[1710,38],[1730,966],[106,1048]])
pts2 = np.float32([[0,0],[WIDTH,0],[WIDTH,HEIGHT],[0,HEIGHT]])

cX = 0; cY = 0; yawAngle = 0; yY = 0; yX = 0;cX_new = 0;cY_new = 0
flag = 0
while(True):
    ret, image = cap.read()

    M = cv2.getPerspectiveTransform(pts1,pts2)
    img = cv2.warpPerspective(image,M,(WIDTH,HEIGHT))

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    ret,thresh = cv2.threshold(imgGray,220,255,cv2.THRESH_BINARY)

    cv2.imshow("ImageGray",thresh)
    if cv2.waitKey(1) == ord('q'):
        break

    _,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 2)

    # print len(contours)

    for i in range(len(contours)):
        c = contours[i]
        area = cv2.contourArea(c)
        # print i,area
        if(area > 3000 and area < 4200):
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # print "cX: ",cX," cY: ",cY

            crop = img[(cY-40):(cY+40),(cX-40):(cX+40)]
            cv2.imshow("Cropped image",crop)
            if cv2.waitKey(1) == ord('q'):
                break
            imgwhiteGray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
            ret,thresh_crop = cv2.threshold(imgwhiteGray,220,255,cv2.THRESH_BINARY)

            _,contours_white,hierarchy_white = cv2.findContours(thresh_crop, cv2.RETR_TREE, 2)

            # print "length: ",len(contours_white)
            count = 0
            # print i
            for j in range(len(contours_white)):
                c_white = contours_white[j]
                area_white = cv2.contourArea(c_white)
                # print "area_white",area_white
                # if(area_white > 1000 and area_white < 4500):
                #     M_White = cv2.moments(c_white)
                #     if M_White["m00"] == 0:
                #         continue
                # cv2.drawContours(crop, [contours_white[j]], -1, (0, 255, 0), 2) #parent - bluish green
                # count = 0
                # for j in range(len(contours_white)):
                    # print hierarchy_white[0][j][2]
                # print hierarchy_white
                if hierarchy_white[0][j][2] == -1 and hierarchy_white[0][j][3] != -1: #Assumption: the small white circles doesnt have any children
                    count += 1
                    if area_white > 250 and area_white < 450:
                        M_small = cv2.moments(contours_white[j])
                        if M_small["m00"] == 0:
                            continue
                        yX = int(M_small["m10"]/M_small["m00"])
                        yY = int(M_small["m01"]/M_small["m00"])
                # elif hierarchy_white[0][j][3] == 0: #Assumption: the outermost contour is always 0
                #     M = cv2.moments(contours_white[j])
                #     if M["m00"] == 0:
                #         continue
                #     cX_new = int(M["m10"]/M["m00"])
                #     cY_new = int(M["m01"]/M["m00"])
                cX_new = 40;    cY_new = 40;
            yawAngle = math.atan2(cY_new-yY,cX_new-yX)*180/math.pi
            print "cX: ",cX," cY: ",cY," cX_new: ",cX_new," cY_new: ",cY_new," yX: ",yX," yY: ",yY," yawAngle: ",yawAngle
            print "Count: ",count
                # print yawAngle

            # cv2.imshow("Image",crop)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     flag = 1
            #     break

#conn.close()
cap.release()
cv2.destroyAllWindows()
