import cv2
from PIL import Image
import time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.ttk import *
import pandas as pd
import numpy as np
import recorder as rc
from tkinter import ttk
import tkinter.messagebox as mb
import traceback
import kociema_module as kc
import colorExtractor as ce
from colorlabeler import cubestr
import kociemba
from tkinter import filedialog
import os
import shutil
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import sqlite3 as sl


con = sl.connect('rubiks.db')


with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS COLORS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            color_name TEXT NOT NULL,
            color_lower TEXT NOT NULL,
            color_upper TEXT NOT NULL
        );
    """)


##with con:
##                 sql="SELECT * FROM NP WHERE number = '"+predicted_result.strip("\n")+"';"
##                 data = con.execute(sql)
##                 for row in data:
##                    print(row)
##                    if row:

#con.execute('DELETE FROM COLORS');
#con.commit()


faces=""
result={}
converted=""
final_string={}
data=""

def convert(string):
    li = list(string.split(" "))
    return li


def toggleSolveText():
    if Solve_button['text'] == 'Solve':
        Solve_button['text'] = 'Solving'
        Record_button['state'] = 'disabled'
    elif Solve_button['text'] == 'Solving':    
        Solve_button['text'] = 'Solve'
        
def toggleEncryptText():
    if Encrypt_button['text'] == 'Encrypt':
        Record_button['state'] = 'disabled'
        Decrypt_button['state'] = 'disabled'
        Encrypt_button['state'] = 'normal'

        
def toggleDecryptText():
    if Decrypt_button['text'] == 'Decrypt':
        Record_button['state'] = 'disabled'
        Decrypt_button['state'] = 'normal'
        Encrypt_button['state'] = 'disabled'

    
def toggleRecordText():
    global converted
    global result
    global data
    #print(result)
    try:
    
        for key in result:
            converted = converted+ result[key]
        if(Record_button['text'][0]!="S"):
            final_string[Record_button['text'][0]]=list(converted)
        converted=""
        #print(final_string)
        if len(final_string)==6:
            data=cubestr(final_string)
            try:
                Solve_label['text'] = str(kociemba.solve(data))
            except Exception as e:
                print(e)
                Solve_label['text'] = str(e)+": Try Again"
            #Record_button['text'] = 'Start Camera'
            #print("here",kociemba.solve(data))
    except Exception as e:
        print(e)
        
    if Record_button['text'] == 'Start Camera':
        Record_button['text'] = 'Front'
    elif Record_button['text'] == 'Front':
        Record_button['text'] = 'Upper'
    elif Record_button['text'] == 'Upper':
        Record_button['text'] = 'Down'
    elif Record_button['text'] == 'Down':
        Record_button['text'] = 'Left'
    elif Record_button['text'] == 'Left':
        Record_button['text'] = 'Right'        
    elif Record_button['text'] == 'Right':
        Record_button['text'] = 'Back'
    elif Record_button['text'] == 'Back':
        Record_button['text'] = 'Recorded'
        
    

        
def toggleCalibrateText():
    print("result",Calibrate_button['text'], result)
    if Calibrate_button['text']!="Calibrate":
        sql = 'INSERT INTO COLORS (color_name, color_lower,color_upper) values(?, ?, ?)'
        data = [str(Calibrate_button['text']),str(result.split('*')[0]),str(result.split('*')[1])]
        with con:
            con.execute(sql, data)
    if Calibrate_button['text'] == 'Calibrate':
        Calibrate_button['text'] = 'Red'
    elif Calibrate_button['text'] == 'Red':
        Calibrate_button['text'] = 'Blue'
    elif Calibrate_button['text'] == 'Blue':
        Calibrate_button['text'] = 'Green'
    elif Calibrate_button['text'] == 'Green':
        Calibrate_button['text'] = 'Yellow'
    elif Calibrate_button['text'] == 'Yellow':
        Calibrate_button['text'] = 'White'        
    elif Calibrate_button['text'] == 'White':
        Calibrate_button['text'] = 'Orange'
    elif Calibrate_button['text'] == 'Orange':
        Calibrate_button['text'] = 'Calibrate'

        
class FileSaver(): 
    def __init__(self):
        file_path=None
        self.file_path=file_path
        self.get_file_path()
        self.save_file()

    def get_file_path(self):
        self.file_path= filedialog.askopenfilename(title = "Select A File")

    def save_file(self):
        global filename
        directory = os.getcwd()
        #print(directory)
        origin=self.file_path
        filename=origin.split('/')[-1]
        target=directory.replace("\\","/")+'/'+filename
        print(origin,target)
        try:
            shutil.copy2(origin,target)
            browse_button['text']=filename
            print(filename)
        except FileNotFoundError:
            print("File not found")


def Encrypter():
    hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None, info=None, backend=default_backend())
    global keye
    print("result_en",result)
    l=""
    for key in result:
        l = l+ result[key]
    print(l)
    keye = base64.urlsafe_b64encode(hkdf.derive(bytes(l,'utf-8')))
    print("enkeye",keye)
    fernet = Fernet(keye)
    with open(filename, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    file.close()
    Solve_label['text'] = "Encrypted"
    Encrypt_button['state'] = 'disabled'
    Decrypt_button['state'] = 'normal'
    


def Decrypter():
    print("result_dec",result)
    l=""
    for key in result:
        l = l+ result[key]
    print(l)
    hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None, info=None, backend=default_backend())
    new_keye = base64.urlsafe_b64encode(hkdf.derive(bytes(l,'utf-8')))
    print("keye",keye)
    print("new_keye",new_keye)
    if not new_keye==keye:
        Solve_label['text'] = "Wrong password"
    else:
        fernet = Fernet(new_keye)
        with open(filename, 'rb') as enc_file:
            encrypted = enc_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(filename, 'wb') as file:
            file.write(decrypted)
        file.close()
        Solve_label['text'] = "Decrypted"
        Encrypt_button['state'] = 'normal'
        Decrypt_button['state'] = 'disabled'

    
def draw_label(face, frame):
        #text = "Class: {}".format(lbl)
        text=str(face)
        pos = (10,30)
        scale = 1
        thickness = 2
        lineType = 2
        fontColor = (0, 0, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,
                    text,
                    pos,
                    font,
                    scale,
                    fontColor,
                    thickness,
                    lineType)
        return frame 

class MainWindow:
    global faces
    def __init__(self,window,cap,action,face,dt):
        self.window = window
        self.cap = cap
        self.action=action
        self.dt=dt
        self.interval = 'idle'
        if result!="Error" and cap.isOpened()==False:
                self.cap=cv2.VideoCapture(0)
        if Record_button['text']!="Start Camera" or  Calibrate_button['text']!="Calibrate":
            print("2",Calibrate_button['text'],Record_button['text'])
            self.update_image()
            
    def update_image(self):
        global result
        global data
        global cap
        try:
            if Record_button['text']!="Start Camera" or Solve_button['text']=="Solving" or Calibrate_button['text']!="Calibrate":
                faces=Record_button['text']
                #print("here")
                self.robj = self.action(self.cap.read()[1],faces[0],self.dt)
                if Solve_button['text']=="Solving" or Calibrate_button['text']!="Calibrate":
                    draw_label("",self.robj.frame)
                else:
                    draw_label("Face: "+faces[0],self.robj.frame)
                result=self.robj.result
                if result=="Completed":
                    Solve_button['text'] = 'Solve'
                    Record_button['state'] = 'normal'
                    Record_button['text'] ='Start Camera'
                elif result=="Error":
                    Solve_button['text'] = 'Solve'
                    Record_button['state'] = 'normal'
                    Record_button['text'] ='Start Camera'
                    self.cap.release()
                    cv2.destroyAllWindows()
                    placeholderImage(self.window)
                elif self.robj != []:
                    try:
                        if self.robj.frame!=[]:
                            #print("jerr")
                            #cv2.imshow("frame",self.robj.frame)
                            #self.frame=cv2.flip(self.frame,1)
                            self.frame=cv2.resize(self.robj.frame,(int(ui_w/1.5),int(ui_h/1.5)))
                            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                            image = Image.fromarray(image)
                            image = ImageTk.PhotoImage(image)
                            self.window.configure(image=image)
                            self.window.image = image
                            self.window.after(self.interval, self.update_image)
                    except Exception as e:
                        print(e)
                        self.cap.release()
                        cv2.destroyAllWindows()
                        placeholderImage(self.window)
                        
            else:
                self.cap.release()
                cv2.destroyAllWindows()
                placeholderImage(self.window)
        except Exception as e:
            print(e)
            traceback.print_exc()
            #self.cap.release()
            print("Error")

    def __del__(self):
        print ('stopped')

                    
def placeholderImage(panel):
    image = cv2.imread('background.png')
    image = cv2.resize(image, (600, 480))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    panel.configure(image=image)
    panel.image = image


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Rubik Cube Solver')
    root.geometry('800x600')
    root.resizable(0, 0)
    ui_w=800
    ui_h=600
    photo = tk.PhotoImage(file = "logo.png")
    root.iconphoto(False, photo)

    style = ttk.Style()
    style.theme_use("xpnative")
    style.map("C.TButton",
            foreground=[('pressed', '#34B7F1'), ('active', 'red')],
            background=[('pressed', 'black'), ('active', '#25D366')]
            )
    style.configure('C.TButton', font=('Helvetica', 15),background="#4876d0")
    style.configure('C.TLabel', font=('Helvetica', 12 ),background="#4876d0" ,foreground="white")
    style.configure('C.TEntry', font=('Helvetica', 12, 'bold'),foreground="#4876d0")
    
    video_window = ttk.Label(root,padding=-2,compound="image")
    video_window.place(x=ui_w/20,y=ui_h/40, width=ui_w/1.5,height=ui_h/1.5)

    cap = cv2.VideoCapture(0)

    Calibrate_button = ttk.Button(root, text="Calibrate", style="C.TButton", command=lambda : [toggleCalibrateText(),MainWindow(video_window,cap,ce.colorExtractor,"","")])
    Calibrate_button.place(x=ui_w/1.3,y=ui_h/35, width=150,height=50)

    Record_button = ttk.Button(root, text="Start Camera", style="C.TButton", command=lambda : [toggleRecordText(),MainWindow(video_window,cap,rc.recorder,"","")])
    Record_button.place(x=ui_w/1.3,y=ui_h/8, width=150,height=50)


    Solve_button = ttk.Button(root, text="Solve", style="C.TButton", command=lambda : [toggleSolveText(),MainWindow(video_window,cap,kc.kociemba_module,"",data)])
    Solve_button.place(x=ui_w/1.3,y=ui_h/4.5, width=150,height=50)

    browse_button = ttk.Button(root, text = "Open File",style="C.TButton",  command=FileSaver)
    browse_button.place(x=ui_w/1.3,y=ui_h/2.9, width=150,height=50)

    Encrypt_button = ttk.Button(root, text="Encrypt", style="C.TButton", command=lambda : [toggleEncryptText(), Encrypter()])
    Encrypt_button.place(x=ui_w/1.3,y=ui_h/2.3, width=150,height=50)

    Decrypt_button = ttk.Button(root, text="Decrypt", style="C.TButton", command=lambda : [toggleDecryptText(), Decrypter()])
    Decrypt_button.place(x=ui_w/1.3,y=ui_h/1.9, width=150,height=50)
    Decrypt_button['state'] = 'disabled'
    
    Solve_label = ttk.Label(root, text="Result Moves will be shown here", style="C.TLabel", anchor=tk.CENTER)
    Solve_label.place(x=ui_w/20,y=ui_h/1.4, width=ui_w/1.1,height=ui_h/5)
    

    root.mainloop()
