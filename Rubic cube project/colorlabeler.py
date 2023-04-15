import numpy as np
import cv2
import sqlite3 as sl
con = sl.connect('rubiks.db')
new={}

def Convert(string):
    
    li = list(string.split(","))
    res = [eval(i) for i in li]
    return res


try:
        with con:
            data = con.execute("SELECT * FROM COLORS")
            for row in data:
                    new[row[1].lower()]=(Convert(row[2]),Convert(row[3]))
                    #print(np.array(row[2]))

except Exception as e:
        print(e)

#print(new)       
bounds =new
##{
##	"red" : (np.array([160, 75, 75]), np.array([180, 255, 255])),
##	"blue" : (np.array([69, 120, 100]), np.array([179, 255, 255])),
##	"green" : (np.array([35, 0, 0]), np.array([85, 255, 255])),
##	"yellow" : (np.array([20, 75, 75]), np.array([40, 255, 255])),
##	"white" : (np.array([0, 0, 20]), np.array([180, 30, 255])),
##	"orange" : (np.array([0, 110, 125]), np.array([17, 255, 255]))
##}


def density(img, color):
	lower = bounds[color][0]
	upper = bounds[color][1]
	#print(np.array(upper),lower)
	mask = cv2.inRange(img, np.array(lower), np.array(upper))
	return np.sum(mask)/255

def cubestr(data):
	ret = ""
	for i in "URFDLB":
		ret += "".join(data[i])
		print(ret)
	for i in "URFDLB":
		ret = ret.replace(data[i][4], i)
		print(ret)
	return ret
