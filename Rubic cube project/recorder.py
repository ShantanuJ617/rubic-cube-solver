import numpy as np
import cv2
import time
from imutils import contours
from colorlabeler import density
from webcolors import rgb_to_name
import kociema_module as kc


class recorder():
    def __init__(self,frame,face,dt):
        self.frame=frame
        self.frame_copy=frame
        self.result="None"
        self.faces=face
        if self.faces!="S":
            self.screen_record()
        
    def screen_record(self):
        last_time = time.time()
        #cv2.startWindowThread()
        #self.faces = "FUDLRB"
        idx = 0

        data = {}

        last_time = time.time()
        img_hsv = cv2.cvtColor(self.frame_copy, cv2.COLOR_BGR2HSV)

        colors = {
                "red" : (0, 0, 255),
                "blue" : (255, 0, 0),
                "green" : (0, 255, 0),
                "yellow" : (0, 0, 0),
                "white" : (255, 255, 255),
                "orange" : (0, 165, 255)
        }

        offset = 75
        z = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                px = 358 + j * offset
                py = 280 + i * offset


                maxDens = [0, "white"]
                crop = img_hsv[(py-35):(py+35), (px-35):(px+35)]
                for k in ("red", "blue", "green", "yellow", "white", "orange"):
                    d = density(crop, k)
                    if d > maxDens[0]:
                        maxDens[0] = d
                        maxDens[1] = k

                cv2.circle(self.frame,(px, py), 5, colors[maxDens[1]], -1)
                data[z] = maxDens[1][0]
                z+=1
            
        self.result=data
                
        return self.frame


