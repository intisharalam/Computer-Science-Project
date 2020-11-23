import face_recognition
import cv2
import os


def GetVideo(path):
    print('Getting Video Feed')
    video = cv2.VideoCapture(path)
    return video

def DrawRectangle(image, match, color, FRAME_THICKNESS, FONT_THICKNESS, face_locations ):
    # Creates a rectangle around the face
    top_left = (face_locations[3], face_locations[0]) # face_locations = [0*top,1*left,2*botton,3*right]
    bottom_right = (face_locations[1], face_locations[2])
    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

    # Creates a filled box with name of the face
    top_left = (face_locations[3], face_locations[2])
    bottom_right = (face_locations[1], face_locations[2] + 15)
    cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
    cv2.putText(image, match, (face_locations[3] + 10, face_locations[2] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250), FONT_THICKNESS)

def VideoImageOperator(image, MODEL, STUDENT_FACE_ENCODINGS, TOLERANCE, COLOR, FRAME_THICKNESS, FONT_THICKNESS, STUDENT_NAMES):
    image = cv2.resize(image, (0,0), None, .25, .25, cv2.INTER_AREA)
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)

    for face_encoding, face_locations in zip(encodings, locations):
        results = face_recognition.compare_faces(STUDENT_FACE_ENCODINGS, face_encoding, TOLERANCE)
        match = None

        if True in results:

            match = STUDENT_NAMES[results.index(True)]
            print(f"Match found: {match}")
            DrawRectangle(image, match, COLOR, FRAME_THICKNESS, FONT_THICKNESS, face_locations)
    return image
