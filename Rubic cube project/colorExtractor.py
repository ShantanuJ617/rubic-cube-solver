import cv2
import numpy as np
from PIL import Image

class colorExtractor():
    x1=100
    x2=150
    y1=150
    y2=200
    x=int((x1+x2)/2)
    y=int((y1+y2)/2)
    result=[]
    def __init__(self,frame,face,dt):
        image_hsv = None
        self.frame=frame
        self.extract()


    def pick_color(self):
            pixel = image_hsv[self.y,self.x]
            upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
            lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
            #print(lower, upper)
            data = np.zeros((50, 50, 3), dtype=np.uint8)
            for i in range(0,50):
                for j in range(0,50):
                    data[i,j] = (upper+lower)/2
            img = Image.fromarray(data, 'HSV')
            self.result=str(pixel[0] - 10)+","+str(pixel[1] - 20)+","+str(pixel[2] - 40)+"*"+str(pixel[0] + 10)+","+str(pixel[1] + 20)+","+str(pixel[2] + 40)
            new=cv2.cvtColor(np.array(img), cv2.COLOR_HSV2BGR)
            cv2.imshow('captured color',new)


 
    def extract(self):
        global image_hsv
        cv2.rectangle(self.frame, (self.x1,self.y1), (self.x2,self.y2), (0, 0, 0), 3)
        image_hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
        self.pick_color()
        return self.frame
    
