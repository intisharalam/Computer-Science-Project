from FaceDetectionAndEncoding import FaceDetectionAndEncoding
from Video_IO import Video_IO

FRAME_THICKNESS = 2
FONT_THICKNESS = 1
MODEL = 'hog' # Model for recognition (cnn is another better alternative --my GPU sucks--)
TOLERANCE = 0.5 # Similarity
COLOUR =  [77, 77,200]
STUDENT_IMAGES_DIR = 'Student_Images'


def main(FRAME_THICKNESS=2, FONT_THICKNESS=1, MODEL='hog', TOLERANCE=0.6, COLOUR=[77,77,255], STUDENT_IMAGES_DIR='Student_Images', VIDEO=0):

    Confirm = input('Do you want reload encodings? \n(y/n): ')
    while Confirm != 'y' and Confirm != 'n':
        print('Invalid Responce! \nTryAgain: ')
        Confirm=input()
    if Confirm == 'y':
        FaceDetectionAndEncoding.EncodeStudentFaceEncoding(STUDENT_IMAGES_DIR)
    
    Name_And_Encodings = FaceDetectionAndEncoding.LoadStudentFaceEncoding()

    Student_Names = Name_And_Encodings[0]
    Student_Face_Encodings = Name_And_Encodings[1]

    video = Video_IO.GetVideo(VIDEO)

    if video == None:
        print('Error Getting Video')
    else:
        FaceDetectionAndEncoding.FaceDetection(TOLERANCE, FRAME_THICKNESS, FONT_THICKNESS, COLOUR, MODEL, video, Student_Face_Encodings, Student_Names)

main(FRAME_THICKNESS, FONT_THICKNESS, MODEL, TOLERANCE, COLOUR,STUDENT_IMAGES_DIR, TEST_VIDEO_DIRECTORY)