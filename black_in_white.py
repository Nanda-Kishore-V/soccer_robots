import cv2
import numpy as np
import math
import time

WIDTH  = 420
HEIGHT = 240

cap = cv2.VideoCapture(1)
cap.set(3,1920) #3 - WIDTH
cap.set(4,1080)  #4 - HEIGHT

pts1 = np.float32([[1300,380],[1720,380],[1720,620],[1300,620]])
pts2 = np.float32([[0,0],[WIDTH,0],[WIDTH,HEIGHT],[0,HEIGHT]])

cX = 0; cY = 0; yawAngle = 0; yY = 0; yX = 0;cX_new = 0;cY_new = 0
flag = 0
while(True):
    ret, image = cap.read()

    M = cv2.getPerspectiveTransform(pts1,pts2)
    img = cv2.warpPerspective(image,M,(WIDTH,HEIGHT))

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #ret,thresh = cv2.threshold(imgGray,65,255,cv2.THRESH_BINARY)
    ret,thresh = cv2.threshold(imgGray,160,255,cv2.THRESH_BINARY)

    # height, width = image.shape[:2]
    # res = cv2.resize(thresh,(int(0.5*width), int(0.5*height)), interpolation = cv2.INTER_CUBIC)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 2)
    # cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imshow('contour', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      	flag = 1
       	break

    # print "Length of contours: ",len(contours)
    for i in range(len(contours)):
        c = contours[i]
        area = cv2.contourArea(c)
        print "i: ",i
        print "Area: ",area
        # print area
        if(area > 8000 and area < 10000):
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            print "cX: ",cX," cY: ",cY

            crop = img[(cY-62):(cY+62),(cX-62):(cX+62)]
            imgwhiteGray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
            ret,thresh_crop = cv2.threshold(imgwhiteGray,160,255,cv2.THRESH_BINARY)


	    #cv2.imshow('fuck', thresh_crop);
            contours_white,hierarchy_white = cv2.findContours(thresh_crop, cv2.RETR_TREE, 2)
            cv2.drawContours(crop, contours_white, -1, (0,255,0), 3)
            cv2.imshow("Crop_with_contour",crop)
    	    if cv2.waitKey(1) & 0xFF == ord('q'):
            	flag = 1
                break
            # print "length: ",len(contours_white)
            count = 0
            print len(contours_white)
            for j in range(len(contours_white)):
                c_white = contours_white[j]
                area_white = cv2.contourArea(c_white)
                print "Area white: ",area_white
                # print "area_white",area_white
                # if(area_white > 1000 and area_white < 4500):
                #     M_White = cv2.moments(c_white)
                #     if M_White["m00"] == 0:
                #         continue
                # cv2.drawContours(crop, [contours_white[j]], -1, (0, 255, 0), 2) #parent - bluish green
                # count = 0
                # for j in range(len(contours_white)):
                    # print hierarchy_white[0][j][2]
                if hierarchy_white[0][j][2] == -1 and area_white > 250: #Assumption: the small white circles doesnt have any children
                    count += 1
                    if area_white > 900 and area_white < 1100:
                        M_small = cv2.moments(contours_white[j])
                        if M_small["m00"] == 0:
                            continue
                        yX = int(M_small["m10"]/M_small["m00"])
                        yY = int(M_small["m01"]/M_small["m00"])
                cX_new = 62;     cY_new = 62
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
