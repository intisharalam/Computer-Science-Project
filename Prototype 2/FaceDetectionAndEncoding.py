import os
import pickle
import numpy as np
from cv2 import imshow, waitKey
from Video_IO import Video_IO

class FaceDetectionAndEncoding:

    def FaceDetection(TOLERANCE, FRAME_THICKNESS, FONT_THICKNESS, COLOR, MODEL, VIDEO, STUDENT_FACE_ENCODINGS, STUDENT_NAMES):
        print('Getting Images From Video Feed \n')
        
        while True:

            ret, image = VIDEO.read()
            image = Video_IO.VideoImageOperator(image, MODEL, STUDENT_FACE_ENCODINGS, TOLERANCE, COLOR, FRAME_THICKNESS, FONT_THICKNESS, STUDENT_NAMES)

            imshow('Test', image)
            if waitKey(1) & 0xFF == ord("q"):
                break


    def LoadStudentFaceEncoding():
        print('Loading Student Faces \n')

        with open('Prototype 2\Student_Encodings.dat', 'rb') as f:
            Loaded_face_encodings = pickle.load(f)

        face_names = list(Loaded_face_encodings.keys())
        face_encodings = np.array(list(Loaded_face_encodings.values()))

        return face_names, face_encodings


    def RecordedEncodingName():
        print('Checking Student Faces Availability \n')

        with open('Prototype 2\Student_Encodings.dat', 'rb') as f:
            Checking_Face_Encodings = pickle.load(f)

        Encoding_names = list(Checking_Face_Encodings.keys())

        return Encoding_names


    def EncodeStudentFaceEncoding(STUDENT_FACE_ENCODINGS_DIR):
        print('Encoding Student Faces \n')

        Loading_Face_Encoding = {}
        NewAdded = False
        EncodedIdentities = FaceDetectionAndEncoding.RecordedEncodingName()
        #print(EncodedIdentities)
        for name in os.listdir(STUDENT_FACE_ENCODINGS_DIR):
            if name not in EncodedIdentities:
                print('New Encoding Is being Added \n')
                NewAdded = True
                for filename in os.listdir(f"{STUDENT_FACE_ENCODINGS_DIR}/{name}"):
                    image = face_recognition.load_image_file(f"{STUDENT_FACE_ENCODINGS_DIR}/{name}/{filename}")
                    location = face_recognition.face_locations(image)
                    encoding = face_recognition.face_encodings(image, location)[0]
                    #print(encoding)
                    Loading_Face_Encoding [name] = encoding
        if NewAdded:
            with open('Prototype 2\Student_Encodings.dat', 'wb') as folder:
                pickle.dump(Loading_Face_Encoding, folder)
        print('Done')

