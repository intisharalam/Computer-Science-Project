import encodings
import face_recognition
from cv2 import rectangle, putText, resize, FONT_HERSHEY_SIMPLEX, FILLED, INTER_AREA, waitKey
# from pathlib import Path
from cv2 import imshow, cv2, VideoCapture, destroyWindow
import numpy as np
from EncodingsDatabaseHandler import EncodingsDB

class FaceRecognition:
    
    FRAME_THICKNESS = 3 # Box frame thickness
    FRAME_COLOUR = [140, 81, 230] # Box colour Lavender Indigo = [140, 81, 230]
    FRAME_WIDTH = 20
    
    TEXT_COLOUR = [255, 255, 255] # Label text colour White = [255, 255, 255]
    FONT_THICKNESS = 2  # Label font thickness
    FONT_SIZE = 0.55 # Label font size
    
    def __init__(self):
        self.frameThickness = self.FRAME_THICKNESS
        self.fontThickness = self.FONT_THICKNESS
        self.boxColour = self.FRAME_COLOUR
        self.txtColour = self.TEXT_COLOUR
        
        self.encodingsDB = EncodingsDB()
        self.encodingsDBData = self.encodingsDB.load_Encodings()
        self.nameList = list(self.encodingsDBData.keys())
        self.encodingsList = np.array(list(self.encodingsDBData.values()))
    
    def drawBox(self, img, faceLocations, text='TEST TXT'):
    
        # Creates a rectangle around the face
        # faceLocations = [0*top,1*left,2*botton,3*right]
        topLeftPos = (faceLocations[3], faceLocations[0]) # top left of the face
        bottomRightPos = (faceLocations[1], faceLocations[2]) # bottom right of the face
        rectangle(img, topLeftPos, bottomRightPos, self.boxColour, self.frameThickness)    # draws a frame starting from top left to bottom right

        # Creates a filled box with name of the face
        right_bottom = (faceLocations[3], faceLocations[2]) # right side of the bottom of the face location from which box will start
        left_bottom = (faceLocations[1], faceLocations[2] + self.FRAME_WIDTH) # left of the bottom side translated by a set amount (the box width) to which box will end
        rectangle(img, right_bottom, left_bottom, self.boxColour, FILLED)  # draws a FILLED box
        
        textXPos = faceLocations[3] + 5 # How far right the text should display along the label box
        textYPos = faceLocations[2] + 15    # How high the text should display along the label box
        putText(img, text, (textXPos, textYPos), FONT_HERSHEY_SIMPLEX, self.FONT_SIZE, self.txtColour, self.fontThickness)

    def faceDetect(self, img):
        faceLocations = face_recognition.face_locations(img)
        faceEncodings = face_recognition.face_encodings(img, faceLocations)
        
        for face_encoding, face_location in zip(faceEncodings, faceLocations):
            results = face_recognition.compare_faces(self.encodingsList, face_encoding)
            matchName = None

            if True in results:
                # match is the name of the identity found
                matchName = self.nameList[results.index(True)]
        
                return face_location, matchName
        return None

# https://www.schemecolor.com/high-contrasts.php link to colour scheme