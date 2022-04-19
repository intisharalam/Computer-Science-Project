import numpy
from pygame import mixer
import time
import cv2
from tkinter import *
import tkinter.messagebox

import os
import pickle
import cv2
import numpy as np
from cv2 import imshow, waitKey
from cv2 import VideoCapture, rectangle, putText, resize, FONT_HERSHEY_SIMPLEX, INTER_AREA, FILLED
from face_recognition import compare_faces, face_locations, face_encodings
from datetime import datetime
import face_recognition

root=Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Driver Cam')
frame.config(background='black')


rootTxt = Tk()
rootTxt.geometry('200x100')

Console = Text(rootTxt)
Console.tag_configure('center', justify='center')
Console.insert('1.0', 'text')
Console.tag_add('center', '1.0', 'end')
Console.pack()

def write(*message, end='\n', sep=' '):
    text = ''
    for item in message:
        text += '{}'.format(item)
        text += sep
    text += end
    Console.insert(INSERT, text)



# Tool bar message box
def Contri():
   tkinter.messagebox.showinfo("Contributors","\n1.Intishar Alam Misbahul\n2.Google\n3.YouTube")

def anotherWin():
   tkinter.messagebox.showinfo("About",'Face Recognition for Attendance v1.0\n Made Using\n-OpenCV\n-Numpy\n-Tkinter\n In Python 3')
                                    
   

# GUI Menu
menu = Menu(root)
root.config(menu=menu)

# Menu toolbar contents

subm1 = Menu(menu)
menu.add_cascade(label="About",menu=subm1)
subm1.add_command(label="Software",command=anotherWin)
subm1.add_command(label="Contributors",command=Contri)


# exit function
def exitt():
   exit()

  
def vid():
   capture =cv2.VideoCapture(0)
   while True:
      ret,frame=capture.read()
      #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      cv2.imshow('frame',frame)
      if cv2.waitKey(1) & 0xFF ==ord('q'):
         break
   capture.release()
   cv2.destroyAllWindows()

def alert():
   mixer.init()
   alert=mixer.Sound('Prototype 1/beep-07.wav')
   alert.play()
   time.sleep(3)
   alert.play()

def load_encoding():
   write('Encoding Student Faces')

   Loading_Face_Encoding = {}
   NewAdded = False
   write('Checking Student Faces Availability')

   with open('Prototype 1/Student_Encodings.dat', 'rb') as f:
      Checking_Face_Encodings = pickle.load(f)

   EncodedIdentities = list(Checking_Face_Encodings.keys())
   for name in os.listdir('Prototype 1/Student_Images'):
      if name not in EncodedIdentities:
         write('New Encoding Is being Added \n')
         NewAdded = True
         for filename in os.listdir(f"Prototype 1/Student_Images/{name}"):
            image = face_recognition.load_image_file(f"Prototype 1/Student_Images/{name}/{filename}")
            location = face_recognition.face_locations(image)
            encoding = face_recognition.face_encodings(image, location)[0]
            Loading_Face_Encoding[name] = encoding
   if NewAdded:
      with open('Prototype 1/Student_Encodings.dat', 'rb') as folder:
         pickle.dump(Loading_Face_Encoding, folder)
   write('Done')


but1=Button(frame,padx=5,pady=5,width=25,bg='white',fg='black',relief=GROOVE,command=vid,text='Open Cam',font=('helvetica 15 bold'))
but1.place(x=100,y=100)

but5=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,text='EXIT',command=exitt,font=('helvetica 15 bold'))
but5.place(x=210,y=400)



rootTxt.mainloop()
root.mainloop()

