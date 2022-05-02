from AttendanceDatabaseHandler import AttendanceDB
from pathlib import Path
from typing import List
import face_recognition
import numpy as np
import os
import pickle
from NotificationSystem import Notify


class EncodingsDB:

    PATH = Path(__file__).resolve().parent  # path to parent folder
    
    def __init__(self):
        self.src = self.PATH / 'Encodings.dat'    # file path to encodings database
        
        self.notify = Notify()
    
    def load_Encodings(self):   # to load data from the Encodings.dat file
        
        if self.src.exists():   # validates if Encodings.dat file exists or not
            with open(self.src, 'rb') as f: # Opens Encodings.dat file as f
                fileData = pickle.load(f)   # Loads file content
            f.close()
            return fileData
        
        else:
            # As pickle cannot load empty binary files, filler content will be loaded after file creation
            fillerDict = {}  # Empty dictionary to store filler encodings
            
            fillerImg = face_recognition.load_image_file(self.PATH / 'fillerImage.jpg') # loads filler image
            imgFaceLoc = face_recognition.face_locations(fillerImg) # stores face locations in the image
            fillerEncodings = face_recognition.face_encodings(fillerImg, imgFaceLoc)[0] # encodes the filler image
            fillerImgName = 'filler Image'  # name for the filler image to used as key in the dictionary
            
            fillerDict[fillerImgName] = fillerEncodings # stores the encodings in the dictionary
            
            newFile = open(self.src, 'wb')   # creates a new file under the file path
            pickle.dump(fillerDict, newFile)    # fills it with filler content
            newFile.close()
            
            newFile = open(self.src, 'rb')  # opens the file again
            fileData = pickle.load(newFile) # loads up the file content
            newFile.close()
            
            # Notifies the user of this error
            self.notify.popUp('Encodings database does not\n exist in directed path.\nNew one has been created instead\nPlease try again!')
            
            return fileData

    def update_Encodings(self):
        
        encodingsData = self.load_Encodings()   # data from the Encodings.dat file which is in the form of a dictionary
        newAdded = False    # initialise flag for new added student images to the students images database
        
        # iterates through list of names of files under Student_Images
        # the files are named after students whose images they contain
        for studentName in os.listdir(self.PATH / 'Student_Images'):    
            if studentName not in list(encodingsData.keys()):   # checks if any name is missing from names of students whose image has been encoded
               newAdded = True  # sets flag to true
            
            for studentImg in os.listdir(self.PATH / 'Student_Images' / studentName):   # iterates through images of the student under their folder
                image = face_recognition.load_image_file(self.PATH / 'Student_Images' / studentName / studentImg)   # loads the image for use
                location = face_recognition.face_locations(image)   # gets the location of the face in the image
                encoding = face_recognition.face_encodings(image, location)[0]  # encodes the face from the image for comparison later on
                encodingsData[studentName] = encoding   # appends the encodings to the dictionary under the student name
        if newAdded:    # checks if flag is set to true
            with open(self.src, 'r+b') as f:
               pickle.dump(encodingsData, f)    # updates the data of Encodings.dat file
            f.close()
        self.notify.popUp('Updated successful', 3000)    # notifies user that the process ended
