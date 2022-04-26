from cv2 import VideoCapture, rectangle, putText, resize, FONT_HERSHEY_SIMPLEX, INTER_AREA, FILLED
from face_recognition import compare_faces, face_locations, face_encodings
from cv2 import imshow, waitKey, cv2
from datetime import datetime
from pygame import mixer
import face_recognition
from tkinter import messagebox
from tkinter import *
from yaml import load
import numpy as np
import tkinter
import shutil
import pickle
import time
import os


root=Tk()
root.geometry('500x570')
root.title('main')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
frame.config(background='black')


# Pop-Up window for aler messages
def popUp(msg):
   popup = Tk()

   popup.title('popUp')
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

def Guide():
   tkinter.messagebox.showinfo(
      "Guide", 
      "\n1. Open Cam - feeds video input from default camera. Show your face to the camera and it will beep if it recognises you.\n2. Encode New Faces - Updates Encoded images file.\n3. Save and Clear - Copies attendance file to SavedAttendance folder and clears all previous attendance record."
      )

def alertSFX():
   mixer.init()
   alert=mixer.Sound('FaceRecog/beep-07.wav')
   alert.play()


# exit function
def Exitt():
   exit()


def saveAndClear():
   
   # Saves the file
   now = datetime.now()
   src = '/home/intishar/Documents/GitHub/Computer-Science-Project/FaceRecog/Attendance.csv'
   newFileName = now.strftime('%a_%d_%b_%Y')
   dst = f'/home/intishar/Documents/GitHub/Computer-Science-Project/FaceRecog/SavedAttendance/Attendance-{newFileName}'

   with open(dst, 'w') as fp:
      pass
   fp.close()

   # open both files
   with open(src,'r') as firstfile, open(dst,'a') as secondfile:
	   # read content from first file
	   for line in firstfile:
		   # append content to second file
		   secondfile.write(line)
   

   # Clears the file
   original = open(src,"w")
   original.close()

   popUp('Done')


def Attendance(name):
   with open('FaceRecog/Attendance.csv', 'r+') as f:
      AttendanceList = f.readlines()
      NameList = []

      for line in AttendanceList:
         entry = line.split(',')
         NameList.append(entry[0])

      if name not in NameList:
         now = datetime.now()
         time = now.strftime('%H:%M')
         date = now.strftime('%d %a %Y')
         f.writelines(f'\n{name},{time},{date}')
   f.close()

def drawBox(img,frame_thickness, font_thickness, txt, faceLoc):
   
   # Creates a rectangle around the face
   top_left = (faceLoc[3], faceLoc[0])  # face_locations = [0*top,1*left,2*botton,3*right]
   bottom_right = (faceLoc[1], faceLoc[2])
   rectangle(img, top_left, bottom_right, [77, 77, 255], frame_thickness)

   # Creates a filled box with name of the face
   top_left = (faceLoc[3], faceLoc[2])
   bottom_right = (faceLoc[1], faceLoc[2] + 15)
   rectangle(img, top_left, bottom_right, [77, 77, 255], FILLED)
   putText(img, txt, (faceLoc[3] + 10, faceLoc[2] + 10), FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250), font_thickness)

def loadEncodings():
   # Loads face encodings stored in .dat file
   with open('FaceRecog/Student_Encodings.dat', 'rb') as f:
      Loaded_face_encodings = pickle.load(f)

      face_names = list(Loaded_face_encodings.keys())
      face_encodings = np.array(list(Loaded_face_encodings.values()))
   f.close()
   return face_names, face_encodings

def encodeFaces():

   Loading_Face_Encoding = {}
   NewAdded = False

   checkFile = 'FaceRecog/Student_Encodings.dat'

   if os.path.isfile(checkFile):
      if os.path.getsize(checkFile) > 0:
         with open('FaceRecog/Student_Encodings.dat', 'rb') as f:
            Checking_Face_Encodings = pickle.load(f)

         EncodedIdentities = list(Checking_Face_Encodings.keys())
         for name in os.listdir('FaceRecog/Student_Images'):
            if name not in EncodedIdentities:
               NewAdded = True
               for filename in os.listdir(f"FaceRecog/Student_Images/{name}"):
                  image = face_recognition.load_image_file(f"FaceRecog/Student_Images/{name}/{filename}")
                  location = face_recognition.face_locations(image)
                  encoding = face_recognition.face_encodings(image, location)[0]
                  Loading_Face_Encoding[name] = encoding
         if NewAdded:
            with open('FaceRecog/Student_Encodings.dat', 'rb') as folder:
               pickle.dump(Loading_Face_Encoding, folder)
         popUp('Done')
      else:
         for name in os.listdir('FaceRecog/Student_Images'):
            for filename in os.listdir(f"FaceRecog/Student_Images/{name}"):
               image = face_recognition.load_image_file(f"FaceRecog/Student_Images/{name}/{filename}")
               location = face_recognition.face_locations(image)
               encoding = face_recognition.face_encodings(image, location)[0]
               Loading_Face_Encoding[name] = encoding
         with open('FaceRecog/Student_Encodings.dat', 'wb') as folder:
               pickle.dump(Loading_Face_Encoding, folder)
         popUp('Done')
   else:
      File = open('FaeRecog/Student_Encodings.dat', 'a')
      File.close()
      popUp("Student Face encodings does not exist \n so new ones are being created. Please Click again to encode fully!")

# Face recognition related functions
def faceRecAndVid():

   FRAME_THICKNESS = 2
   FONT_THICKNESS = 1
   MODEL = 'hog'  # Model for recognition cnn/hog
   TOLERANCE = 0.5  # Similarity
   COLOUR = [77, 77, 200] # shade of red


   Student_Names, Student_Face_Encodings = loadEncodings()

   video = VideoCapture(0)


   if video is None:
      popUp('Error Getting Video')
   else:
      while True:
         ret, image = video.read()

         if ret == True:
            image = resize(image, (0, 0), None, .75, .75, INTER_AREA)
            image = cv2.flip(image, 1)  # not use cv2.rotate(img, deg) / -1 flips it over
            locations = face_recognition.face_locations(image, model=MODEL)
            encodings = face_recognition.face_encodings(image, locations)

            for face_encoding, face_locations in zip(encodings, locations):
               results = compare_faces(Student_Face_Encodings, face_encoding, TOLERANCE)
               match = None

               if True in results:
                  # match is the name of the identity found
                  match = Student_Names[results.index(True)]
                  Attendance(match)
                  drawBox(image, FRAME_THICKNESS, FONT_THICKNESS, match, face_locations)
                  alertSFX()
                  imshow('Test', image)
                  waitKey(500)

            imshow('Test', image)
            if waitKey(1) & 0xFF == ord("q"):
               video.release()
               cv2.destroyWindow('Test')
               popUp('Done')
               break
         else:
            video.release()
            popUp('Error getting Video')
            break


# GUI Menu
menu = Menu(root)
root.config(menu=menu)

# Menu toolbar contents
subm1 = Menu(menu)
subm1.add_command(label="Software",command=About)
subm1.add_command(label="Contributors",command=Contri)
menu.add_cascade(label="About",menu=subm1)

subm2 = Menu(menu)
subm2.add_command(label="Guide",command=Guide)
menu.add_cascade(label="Help",menu=subm2)


but1=Button(frame,padx=5,pady=5,width=25,bg='white',fg='black',relief=GROOVE,command=faceRecAndVid,text='Open Cam',font=('helvetica 15 bold'))
but1.place(x=100,y=100)

but2=Button(frame,padx=5,pady=5,width=25,bg='white',fg='black',relief=GROOVE,command=encodeFaces,text='Encode New Faces',font=('helvetica 15 bold'))
but2.place(x=100,y=180)

but3=Button(frame,padx=5,pady=5,width=25,bg='white',fg='black',relief=GROOVE,command=saveAndClear,text='Save and Clear',font=('helvetica 15 bold'))
but3.place(x=100,y=260)

but4=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,text='EXIT',command=Exitt,font=('helvetica 15 bold'))
but4.place(x=210,y=360)


root.mainloop()