import cv2
import time
import numpy as np
import random

vid = cv2.VideoCapture('footage.mp4')

index=0
index1=0

class balls:

    def __init__(self,x,y,velocity):
        global index1
        self.img=img
        self.vx =  - velocity/5 + random.random() * 4
        self.vy = random.random() * 5
        self.x  = x
        self.y = y
        self.friction = 0
        self.gravity = 0.01
        self.radius = int(random.random() * 15)
        index1 = index1 + 1
        if index1>255:
            index1=0
        #self.color=[index1+1,255-index1,int(1.5*(128-index1) if index1<128 else 1.5*(index1-128))]
        self.color=[int(255*random.random()),int(255*random.random()),int(255*random.random())]

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

locus=[]

img_array=[]

out = cv2.VideoWriter('output2.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 60, (500,500))


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
            velocity = xx-pre_xx
            pre_xx = xx
            #print(xx,yy)
            #print(velocity)
            ball_holder.append(balls(xx,yy,velocity))
            if len(ball_holder)>balls_life:
                ball_holder.remove(ball_holder[0])

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
            cv2.line(frame, point_1, point_2, [125, 60, 128], 2)
            cv2.line(frame, point_2, point_3, [125, 60, 128], 2)
            m1=(point_2[1]-point_1[1])/(point_2[0]-point_1[0])
            m1=-1/m1
            mid_1=[int((point_1[0]+point_2[0])/2),int((point_1[1]+point_2[1])/2)]

            cv2.line(frame, mid_1,[mid_1[0]+150,int(mid_1[1]+150*m1)], [255, 0, 0], 2)

            m2=(point_3[1]-point_2[1])/(point_3[0]-point_2[0])
            m2=-1/m2
            mid_2=[int((point_2[0]+point_3[0])/2),int((point_2[1]+point_3[1])/2)]
            #print(mid_1,m1,mid_2,m2)
            cv2.line(frame, mid_2,[mid_2[0]-100,int(mid_2[1]-100*m2)], [255, 0, 0], 2)
            cv2.circle(frame, [254, 20], 10, [0,0,255],3)

            cv2.line(frame, [254, 20],[xx,300+yy],[50, 250, 65], 3)
            cv2.circle(frame, [xx, 300+yy], 20, [200, 200, 0], 5)

            length_of_string = int(((locus[0][0]-254)**2+(locus[0][1]-20)**2)**0.5)
            frame = cv2.putText(frame, 'Length = '+str(length_of_string)+'px', (10,30),
                             cv2.FONT_HERSHEY_SIMPLEX,.7, [0,0,255], 1, cv2.LINE_AA)

        for i in ball_holder:
            i.update()
            i.draw(img)

        cv2.imshow('Frame',frame)
        img_array.append(frame)
        out.write(frame)

        index=index+1
        #print(index)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        print('breaking...')
        break

print('release started')
out.release()

print('release end')
vid.release()
cv2.destroyAllWindows()