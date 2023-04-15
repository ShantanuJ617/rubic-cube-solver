import kociemba
import cv2
import numpy as np
import time
from rubik_solver import utils
from drawLine import *
#import winsound


class kociemba_module():
    frame_idx = 0
    frame_reset_cnt = 20
    result_index = 0
    
    
    startpoint = (100, 100)
    
    cubeImg = np.zeros((480,640))
    def __init__(self,frame,face,dt):
        self.frame=frame
        self.color_list=dt
        if self.frame!=[]:
            self.kociema()

        
    def convert(self,a):
        li = list(a.split(" "))
        return li

    def kociema(self):
            import kociemba
            cube = ""
            result_string=[]
            for i in self.color_list:
                    cube = cube + i
            #print("cube",cube)
            try:
                a= kociemba.solve(cube)
            except Exception as e:
                print(e)
                self.frame=[]
                self.result="Error"
                return
            #print("koci",a)
            result_string = self.convert(a)
            #print("result_string",result_string)
            
            for i in result_string:
                    i = str(i)
                    if len(i) > 1:
                            if i[1] == '2':
                                    
                                    s = i[0]
                                    index = result_string.index(i)
                                    result_string.remove(i)
                                    result_string.insert(index,s)
                                    result_string.insert(index,s)
                            elif i == "B'":
                                    index = result_string.index(i)
                                    result_string.remove(i)
                                    # replace B' with 3 instructions B' ==> up, right, down
                                    result_string.insert(index, "up")
                                    result_string.insert(index, "U'")
                                    result_string.insert(index, "down")

                    elif i == "B":
                            index = result_string.index(i)
                            result_string.remove(i)
                            # replace B with 3 instructions B ==> up, left, down
                            result_string.insert(index, "up")
                            result_string.insert(index, "U")
                            result_string.insert(index, "down")
                    else:
                            continue

            cubeshape = 180
            cubesize = 3
            #print(result_string)
            cubeImg=self.frame
            #cv2.waitKey(10)
            #cv2.imshow("cube",cubeImg)
            drawCube(cubeImg,cubeshape,cubesize,self.startpoint)
            #print("len(result_string)",len(result_string))
            #print("result_index",result_index)

            if self.result_index >= len(result_string)-1:
                    cv2.putText(cubeImg, "Solved", (int(cubeImg.shape[1]/4), 30), cv2.FONT_HERSHEY_COMPLEX,1.5, (0,255,0))
                    #cv2.imshow("cube", cubeImg)
                    self.result="Completed"
                

            self.__class__.frame_idx += 1
            if self.frame_idx > self.frame_reset_cnt:
                    #winsound.Beep(500,300)
                    cv2.putText(cubeImg, "Next", (int(cubeImg.shape[1]/4), 30), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,255,0))
                    self.__class__.result_index += 1
                    self.__class__.frame_idx = 0

            #print("result_index",self.result_index)
            #print("frame_idx",self.frame_idx)
            #print("frame_reset_cnt",self.frame_reset_cnt)
            self.result="None"
            try:
                res = result_string[self.result_index]
                if res == "D":
                    arrowlines(cubeImg,(2,0),(2,2), cubeshape, cubesize)

                elif res == "D'":
                        arrowlines(cubeImg,(2,2),(2,0), cubeshape, cubesize)
                
                elif res == 'F':
                        rotation(cubeImg)

                elif res == "F'":
                        antirotation(cubeImg)

                elif res == 'R':
                        arrowlines(cubeImg,(2,2),(0,2), cubeshape, cubesize)

                elif res == "R'":
                        arrowlines(cubeImg,(0,2),(2,2), cubeshape, cubesize)

                elif res == 'U':
                        arrowlines(cubeImg,(0,2),(0,0), cubeshape, cubesize)

                elif res == "U'":
                        arrowlines(cubeImg,(0,0),(0,2), cubeshape, cubesize)
                
                elif res == 'L':
                        arrowlines(cubeImg,(0,0),(2,0), cubeshape, cubesize)

                elif res == "L'":
                        arrowlines(cubeImg,(2,0),(0,0), cubeshape, cubesize)

                elif res == "down":
                        arrowlines(cubeImg,(0,0),(2,0), cubeshape, cubesize)
                        arrowlines(cubeImg,(0,1),(2,1), cubeshape, cubesize)
                        arrowlines(cubeImg,(0,2),(2,2), cubeshape, cubesize)

                elif res == "up":
                        arrowlines(cubeImg,(2,0),(0,0), cubeshape, cubesize)
                        arrowlines(cubeImg,(2,1),(0,1), cubeshape, cubesize)
                        arrowlines(cubeImg,(2,2),(0,2), cubeshape, cubesize)

                elif res == "right":
                        arrowlines(cubeImg,(0,0),(0,2), cubeshape, cubesize)
                        arrowlines(cubeImg,(1,0),(1,2), cubeshape, cubesize)
                        arrowlines(cubeImg,(2,0),(2,2), cubeshape, cubesize)

                elif res == "left":
                        arrowlines(cubeImg,(0,2),(0,0), cubeshape, cubesize)
                        arrowlines(cubeImg,(1,2),(1,0), cubeshape, cubesize)
                        arrowlines(cubeImg,(2,2),(2,0), cubeshape, cubesize)
            except Exception as e:
                self.result="Completed"
                print(e)
            
            
            

            
            self.frame=cubeImg
            #cv2.imshow("frame",self.frame)
            #cv2.waitKey(1)
            return self.frame
