import os
import pickle
import numpy as np
from cv2 import imshow, waitKey
from cv2 import VideoCapture, rectangle, putText, resize, FONT_HERSHEY_SIMPLEX, INTER_AREA, FILLED
from face_recognition import compare_faces, face_locations, face_encodings
from datetime import datetime
import face_recognition

FRAME_THICKNESS = 2
FONT_THICKNESS = 1
MODEL = 'hog' # Model for recognition (cnn is another better alternative --my GPU sucks--)
TOLERANCE = 0.5 # Similarity
COLOUR =  [77, 77,200]
STUDENT_IMAGES_DIR = 'Student_Images'
TEST_VIDEO_DIRECTORY = 0 #'Test_Stuff\TestVids\obama.mp4'


Confirm = input('Do you want reload encodings? \n(y/n): ')
while Confirm != 'y' and Confirm != 'n':
    print('Invalid Responce! \nTryAgain: ')
    Confirm=input()
if Confirm == 'y':
    print('Encoding Student Faces \n')

    Loading_Face_Encoding = {}
    NewAdded = False
    print('Checking Student Faces Availability \n')

    with open('Face Recognition For Attendance Project\Student_Encodings.dat', 'rb') as f:
        Checking_Face_Encodings = pickle.load(f)

    EncodedIdentities = list(Checking_Face_Encodings.keys())
    for name in os.listdir(STUDENT_FACE_ENCODINGS_DIR):
        if name not in EncodedIdentities:
            print('New Encoding Is being Added \n')
            NewAdded = True
            for filename in os.listdir(f"{STUDENT_FACE_ENCODINGS_DIR}/{name}"):
                image = face_recognition.load_image_file(f"{STUDENT_FACE_ENCODINGS_DIR}/{name}/{filename}")
                location = face_recognition.face_locations(image)
                encoding = face_recognition.face_encodings(image, location)[0]
                Loading_Face_Encoding [name] = encoding
    if NewAdded:
        with open('Face Recognition For Attendance Project\Student_Encodings.dat', 'wb') as folder:
            pickle.dump(Loading_Face_Encoding, folder)
    print('Done')


print('Loading Student Faces \n')

with open('Face Recognition For Attendance Project\Student_Encodings.dat', 'rb') as f:
    Loaded_face_encodings = pickle.load(f)

    face_names = list(Loaded_face_encodings.keys())
    face_encodings = np.array(list(Loaded_face_encodings.values()))

Name_And_Encodings = face_names, face_encodings

Student_Names = Name_And_Encodings[0]
Student_Face_Encodings = Name_And_Encodings[1]

print('Getting Video Feed \n')
video = VideoCapture(0)

if video == None:
    print('Error Getting Video')
else:
    print('Getting Images From Video Feed \n')
    
    while True:
        ret, image = video.read()
        image = resize(image, (0,0), None, .3, .3, INTER_AREA)
        locations = face_recognition.face_locations(image, model=MODEL)
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_locations in zip(encodings, locations):
            results = compare_faces(Student_Face_Encodings, face_encoding, TOLERANCE)
            match = None

            if True in results:
                # match is the name of the identity found
                match = Student_Names[results.index(True)]
                with open('Face Recognition For Attendance Project\Attendance.csv', 'r+') as f:
                    AttendanceList = f.readlines()
                    NameList = []
                    for line in AttendanceList:
                        entry = line.split(',')
                        NameList.append(entry[0])
                    if match not in NameList:
                        now = datetime.now()
                        CurrentString = now.strftime('%H:%M')
                        f.writelines(f'\n{name},{CurrentString}')
                print(f"Match found: {match}")
                # Creates a rectangle around the face
                top_left = (face_locations[3], face_locations[0]) # face_locations = [0*top,1*left,2*botton,3*right]
                bottom_right = (face_locations[1], face_locations[2])
                rectangle(image, top_left, bottom_right, [77,77,255], FRAME_THICKNESS)

                # Creates a filled box with name of the face
                top_left = (face_locations[3], face_locations[2])
                bottom_right = (face_locations[1], face_locations[2] + 15)
                rectangle(image, top_left, bottom_right, [77,77,255], FILLED)
                putText(image, match, (face_locations[3] + 10, face_locations[2] + 10), FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250), FONT_THICKNESS)

        imshow('Test', image)
        if waitKey(1) & 0xFF == ord("q"):
            break