import FaceDetectAndEncoding
import Video_IO

FRAME_THICKNESS = 2
FONT_THICKNESS = 1
MODEL = 'hog' # Model for recognition (cnn is another better alternative --my GPU sucks--)
TOLERANCE = 0.6 # Similarity
COLOUR =  [77, 77,200]
STUDENT_IMAGES_DIR = 'Student_Images'
TEST_VIDEO_DIRECTORY = 'Test_Stuff\TestVids\Obama.mp4'


Confirm = input('Do you want reload encodings? \n (y/n): ')
if Confirm == 'y':
    FaceDetectAndEncoding.EncodeStudentFaceEncoding(STUDENT_IMAGES_DIR)

Name_And_Encodings = FaceDetectAndEncoding.LoadStudentFaceEncoding(STUDENT_IMAGES_DIR)

Student_Names = Name_And_Encodings[0]
Student_Face_Encodings = Name_And_Encodings[1]

video = Video_IO.GetVideo(TEST_VIDEO_DIRECTORY)

if video == None:
    print('Error Getting Video')
else:
    FaceDetectAndEncoding.FaceDetection(TOLERANCE, FRAME_THICKNESS, FONT_THICKNESS, COLOUR, MODEL, video, Student_Face_Encodings, Student_Names)
