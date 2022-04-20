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
from yaml import load

root=Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
frame.config(background='black')


# Pop-Up window for aler messages
def popUp(msg):
   popup = Tk()

   label = Label(popup, text=msg)
   label.pack(side='top', fill='x', pady=10)
   B1 = Button(popup, text = 'Ok', command = popup.destroy)
   B1.pack()
   popup.mainloop()


# Tool bar message box
def Contri():
   tkinter.messagebox.showinfo("Contributors","\n1.Intishar Alam Misbahul\n2.Google\n3.YouTube")

def About():
   tkinter.messagebox.showinfo("About",'Face Recognition for Attendance v1.0\n Made Using\n-OpenCV\n-Numpy\n-Tkinter\n In Python 3')


# exit function
def Exitt():
   exit()

# Face recognition related functions
def Vid():
   capture =cv2.VideoCapture(0)
   while True:
      ret,frame=capture.read()
      #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      cv2.imshow('frame',frame)
      if cv2.waitKey(1) & 0xFF ==ord('q'):
         break
   capture.release()
   cv2.destroyAllWindows()

def alertSFX():
   mixer.init()
   alert=mixer.Sound('Prototype 1/beep-07.wav')
   alert.play()
   time.sleep(3)
   alert.play()

def encodeFaces():

   Loading_Face_Encoding = {}
   NewAdded = False

   checkFile = 'Prototype 1/Student_Encodings.dat'

   if os.path.isfile(checkFile):
      if os.path.getsize(checkFile) > 0:
         with open('Prototype 1/Student_Encodings.dat', 'rb') as f:
            Checking_Face_Encodings = pickle.load(f)

         EncodedIdentities = list(Checking_Face_Encodings.keys())
         for name in os.listdir('Prototype 1/Student_Images'):
            if name not in EncodedIdentities:
               NewAdded = True
               for filename in os.listdir(f"Prototype 1/Student_Images/{name}"):
                  image = face_recognition.load_image_file(f"Prototype 1/Student_Images/{name}/{filename}")
                  location = face_recognition.face_locations(image)
                  encoding = face_recognition.face_encodings(image, location)[0]
                  Loading_Face_Encoding[name] = encoding
         if NewAdded:
            with open('Prototype 1/Student_Encodings.dat', 'rb') as folder:
               pickle.dump(Loading_Face_Encoding, folder)
         popUp('Done')
      else:
         for name in os.listdir('Prototype 1/Student_Images'):
            for filename in os.listdir(f"Prototype 1/Student_Images/{name}"):
               image = face_recognition.load_image_file(f"Prototype 1/Student_Images/{name}/{filename}")
               location = face_recognition.face_locations(image)
               encoding = face_recognition.face_encodings(image, location)[0]
               Loading_Face_Encoding[name] = encoding
         with open('Prototype 1/Student_Encodings.dat', 'wb') as folder:
               pickle.dump(Loading_Face_Encoding, folder)
         popUp('Done')
   else:
      File = open('Prototype 1/Student_Encodings.dat', 'a')
      File.close()
      popUp("Specified file does not exist!\n And will be created!\n Please try again AFTER encoding with new images!")



# GUI Menu
menu = Menu(root)
root.config(menu=menu)


# Menu toolbar contents
subm1 = Menu(menu)
menu.add_cascade(label="About",menu=subm1)
subm1.add_command(label="Software",command=About)
subm1.add_command(label="Contributors",command=Contri)



but1=Button(frame,padx=5,pady=5,width=25,bg='white',fg='black',relief=GROOVE,command=Vid,text='Open Cam',font=('helvetica 15 bold'))
but1.place(x=100,y=100)

but2=Button(frame,padx=5,pady=5,width=25,bg='white',fg='black',relief=GROOVE,command=encodeFaces,text='Encode New Faces',font=('helvetica 15 bold'))
but2.place(x=100,y=140)

but5=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,text='EXIT',command=Exitt,font=('helvetica 15 bold'))
but5.place(x=210,y=180)


root.mainloop()