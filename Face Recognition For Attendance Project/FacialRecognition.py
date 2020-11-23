from cv2 import imshow, waitKey, VideoCapture, rectangle, putText, resize, FONT_HERSHEY_SIMPLEX, INTER_AREA, FILLED
from face_recognition import compare_faces, face_locations, face_encodings
import face_recognition
import numpy as np
import pickle
import os

class FaceDetectionAndEncoding:

    def FaceDetection(TOLERANCE, FRAME_THICKNESS, FONT_THICKNESS, COLOR, MODEL, VIDEO, STUDENT_FACE_ENCODINGS, STUDENT_NAMES):
        print('Getting Images From Video Feed')
        
        while True:

            ret, image = VIDEO.read()
            image = Video_IO.VideoImageOperator(image, MODEL, STUDENT_FACE_ENCODINGS, TOLERANCE, COLOR, FRAME_THICKNESS, FONT_THICKNESS, STUDENT_NAMES)

            imshow('Test', image)
            if waitKey(1) & 0xFF == ord("q"):
                break

    def LoadStudentFaceEncoding():
        print('Loading Student Faces')

        with open('Student_Face_Encodings/Student_Encodings.dat', 'rb') as f:
            Loaded_face_encodings = pickle.load(f)

        face_names = list(Loaded_face_encodings.keys())
        face_encodings = np.array(list(Loaded_face_encodings.values()))

        return face_names, face_encodings

    def EncodeStudentFaceEncoding(STUDENT_FACE_ENCODINGS_DIR):
        print('Encoding Student Faces')

        Loading_Face_Encoding = {}

        for name in os.listdir(STUDENT_FACE_ENCODINGS_DIR):
            for filename in os.listdir(f"{STUDENT_FACE_ENCODINGS_DIR}/{name}"):
                image = face_recognition.load_image_file(f"{STUDENT_FACE_ENCODINGS_DIR}/{name}/{filename}")
                location = face_recognition.face_locations(image)
                encoding = face_recognition.face_encodings(image, location)[0]
                print(encoding)
                Loading_Face_Encoding [name] = encoding

        with open('Student_Face_Encodings/Student_Encodings.dat', 'wb') as folder:
            pickle.dump(Loading_Face_Encoding, folder)
        print('Done')


class Video_IO:

    def GetVideo(path):
        print('Getting Video Feed')
        video = VideoCapture(path)
        return video

    def DrawRectangle(image, match, color, FRAME_THICKNESS, FONT_THICKNESS, face_locations ):
        # Creates a rectangle around the face
        top_left = (face_locations[3], face_locations[0]) # face_locations = [0*top,1*left,2*botton,3*right]
        bottom_right = (face_locations[1], face_locations[2])
        rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

        # Creates a filled box with name of the face
        top_left = (face_locations[3], face_locations[2])
        bottom_right = (face_locations[1], face_locations[2] + 15)
        rectangle(image, top_left, bottom_right, color, FILLED)
        putText(image, match, (face_locations[3] + 10, face_locations[2] + 10), FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250), FONT_THICKNESS)

    def VideoImageOperator(image, MODEL, STUDENT_FACE_ENCODINGS, TOLERANCE, COLOR, FRAME_THICKNESS, FONT_THICKNESS, STUDENT_NAMES):
        image = resize(image, (0,0), None, .25, .25, INTER_AREA)
        locations = face_recognition.face_locations(image, model=MODEL)
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_locations in zip(encodings, locations):
            results = compare_faces(STUDENT_FACE_ENCODINGS, face_encoding, TOLERANCE)
            match = None

            if True in results:

                match = STUDENT_NAMES[results.index(True)]
                print(f"Match found: {match}")
                Video_IO.DrawRectangle(image, match, COLOR, FRAME_THICKNESS, FONT_THICKNESS, face_locations)
        return image
