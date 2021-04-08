from cv2 import VideoCapture, rectangle, putText, resize, FONT_HERSHEY_SIMPLEX, INTER_AREA, FILLED
from face_recognition import compare_faces, face_locations, face_encodings
from Attendance import Attendance
import face_recognition

class Video_IO:
    
    def GetVideo(path=0):
        print('Getting Video Feed \n')
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
        image = resize(image, (0,0), None, .3, .3, INTER_AREA)
        locations = face_recognition.face_locations(image, model=MODEL)
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_locations in zip(encodings, locations):
            results = compare_faces(STUDENT_FACE_ENCODINGS, face_encoding, TOLERANCE)
            match = None

            if True in results:
                # match is the name of the identity found
                match = STUDENT_NAMES[results.index(True)]
                Attendance.MarkAttendance(match)
                print(f"Match found: {match}")
                Video_IO.DrawRectangle(image, match, COLOR, FRAME_THICKNESS, FONT_THICKNESS, face_locations)
        return image
