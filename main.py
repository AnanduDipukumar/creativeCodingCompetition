import cv2
import time
import numpy as np
import random

vid = cv2.VideoCapture('footage.mp4')

index=0

class balls:

    def __init__(self,x,y,velocity):
        global index
        self.img=img
        self.vx =  - velocity/5 + random.random() * 3
        self.vy = random.random() * 5
        self.x  = x
        self.y = y
        self.friction = 0
        self.gravity = 0.01
        self.radius = int(random.random() * 15)
        index = index + 1
        if index>255:
            index=0
        self.color=[index+1,255-index,int(1.5*(128-index) if index<128 else 1.5*(index-128))]
        #self.color=[int(255*random.random()),int(255*random.random()),int(255*random.random())]

    def update(self):
        self.x = max(int(self.x + self.vx),0)
        self.y = max(int(self.y + self.vy),0)
        #self.vx = self.vx - self.friction
        self.vy = self.vy + self.gravity

    def draw(self,img):
        cv2.circle(frame, [self.x, 300 + self.y], self.radius,self.color, int(self.radius/5)+1)

ball_holder=[]

balls_life = 100

pre_xx =0

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
            velocity = xx-pre_xx
            pre_xx = xx
            #print(xx,yy)
            print(velocity)
            ball_holder.append(balls(xx,yy,velocity))
            if len(ball_holder)>balls_life:
                ball_holder.remove(ball_holder[0])

        for i in ball_holder:
            i.update()
            i.draw(img)

        cv2.imshow('Frame',frame)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()