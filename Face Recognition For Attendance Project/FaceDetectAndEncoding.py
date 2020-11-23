from Video_IO import VideoImageOperator
import face_recognition
import numpy as np
import pickle
import cv2
import os


def FaceDetection(TOLERANCE, FRAME_THICKNESS, FONT_THICKNESS, COLOR, MODEL, VIDEO, STUDENT_FACE_ENCODINGS, STUDENT_NAMES):
    print('Getting Images From Video Feed')
    while True:

        ret, image = VIDEO.read()
        image = VideoImageOperator(image, MODEL, STUDENT_FACE_ENCODINGS, TOLERANCE, COLOR, FRAME_THICKNESS, FONT_THICKNESS, STUDENT_NAMES)

        cv2.imshow('Test', image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

def LoadStudentFaceEncoding(STUDENT_FACE_ENCODINGS_DIR):
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
    