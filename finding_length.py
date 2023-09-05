import cv2
import time
import numpy as np
import random

vid = cv2.VideoCapture('footage.mp4')

index=0

locus=[]

while (vid.isOpened()):
    # Capture frame-by-frame
    ret, frame = vid.read()
    if ret == True:

        # Display the resulting frame
        img=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #print(img.shape)
        img[300:][img[300:]<180]=0
        mask=img[300:]<180

        mask=mask.astype('uint8')*255
        #print(type(mask[0][0]))
        y,x = np.where(mask == 255)
        size=x.shape

        if size[0]>0:
            xx=int(np.sum(x)/size)
            yy=int(np.sum(y)/size)
            #print(xx,yy)

        if index > 85 and index< 125:
            locus.append([xx,300+yy])
            for i in range(len(locus)-1):
                cv2.line(frame, locus[i], locus[i+1], [0,0,255], 2)
        elif index>125:
            for i in range(len(locus) - 1):
                cv2.line(frame, locus[i], locus[i + 1], [0, 0, 255], 2)
            point_1=locus[0]
            point_3=locus[125-85-2]
            point_2 = locus[15]
            cv2.line(frame, point_1, point_2, [255, 0, 0], 2)
            cv2.line(frame, point_2, point_3, [255, 0, 0], 2)
            m1=(point_2[1]-point_1[1])/(point_2[0]-point_1[0])
            m1=-1/m1
            mid_1=[int((point_1[0]+point_2[0])/2),int((point_1[1]+point_2[1])/2)]

            cv2.line(frame, mid_1,[mid_1[0]+150,int(mid_1[1]+150*m1)], [0, 255, 0], 2)

            m2=(point_3[1]-point_2[1])/(point_3[0]-point_2[0])
            m2=-1/m2
            mid_2=[int((point_2[0]+point_3[0])/2),int((point_2[1]+point_3[1])/2)]

            cv2.line(frame, mid_2,[mid_2[0]-100,int(mid_2[1]-100*m2)], [0, 255, 0], 2)

        cv2.imshow('Frame',frame)

        index=index+1
        #print(index)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()