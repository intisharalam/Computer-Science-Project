from tkinter import messagebox
import tkinter as tk
import PIL.Image, PIL.ImageTk
from cv2 import CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH, COLOR_BGR2RGB, VideoCapture, cvtColor, flip
from EncodingsDatabaseHandler import EncodingsDB
from AttendanceDatabaseHandler import AttendanceDB
from NotificationSystem import Notify
from FacialRecognition import FaceRecognition


# Inherit from Tk class for creating toplevel widget / main window
class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        # inherit __init__ function from tk.Tk class
        tk.Tk.__init__(self, *args, **kwargs)
        
        # setting root window size and title
        self.geometry('500x600')
        self.title('main')
        
        # creates a container frame        
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = 1)
        
        # create a 1x1 grid for fitting in frames
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        # initialising an array for multiple frames/windows
        self.frames = {}
        
        # Iterates through a turple of different page layout aka windows
        for F in (MainScreen, VideoFeed):

            frame = F(container, self)
            
            # initialises the object for each page layout
            self.frames[F] = frame
            # positions them in a grid
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        # displays the first page to be seen by the user
        self.showFrame(MainScreen)
    
    #display the frame/object passed to it as parameter
    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
        #   displays the menubar
        menubar = frame.menuBar(self)
        self.config(menu=menubar)

class MainScreen(tk.Frame):
    
    def __init__(self, parent, controller):
        # inherit __init__ function from tk.Tk class
        tk.Frame.__init__(self, parent)
        
        # set background to black
        self.config(background = 'black')
        
        # initiating classes
        self.encodingsManager = EncodingsDB()
        self.attendanceManager = AttendanceDB()
        self.notify = Notify()
        
        # configures the grid rows and column so that
        # it takes all available space and is resizable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # menu buttons
        but1=tk.Button(self,padx=5,pady=5,height=2,width=15,bg='white',fg='black',relief='groove',text='Open Cam',font=('helvetica 15 bold'),command=lambda : controller.showFrame(VideoFeed))
        but1.grid(column=0, row=0)

        but2=tk.Button(self,padx=5,pady=5,height=2,width=15,bg='white',fg='black',relief='groove',text='Encode New Faces',font=('helvetica 15 bold'),command=lambda :self.encodingsManager.update_Encodings())
        but2.grid(column=0, row=1)

        but3=tk.Button(self,padx=5,pady=5,height=2,width=15,bg='white',fg='black',relief='groove',text='Save and Clear',font=('helvetica 15 bold'),command=lambda :self.attendanceManager.save_Attendance())
        but3.grid(column=0, row=2)

        but4=tk.Button(self,padx=5,pady=5,height=2,width=15,bg='white',fg='black',relief='groove',text='EXIT',font=('helvetica 15 bold'),command=lambda :self.Eexit())
        but4.grid(column=0, row=3)
    
    # for stopping the software
    def Eexit(self):
        exit()
    
    # creates the menubar
    def menuBar(self, root):
            
        menubar = tk.Menu(root, bd = 100)
        
        aboutMenu = tk.Menu(menubar, tearoff = 0)
        helpMenu = tk.Menu(menubar, tearoff = 0)
        
        menubar.add_cascade(label="About", menu=aboutMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)
        
        aboutMenu.add_command(label = 'Software', command = self.aboutSoftware)
        aboutMenu.add_command(label = 'Contributors', command = self.aboutContributors)
        
        helpMenu.add_command(label = 'How to Use', command = self.howToUse)
        
        return menubar
    
    # menu elements
    def aboutSoftware(self):
        messagebox.showinfo('Software', 'Face Recognition for Attendance v1.0\n Made Using:\n-OpenCV\n-Numpy\n-Tkinter In Python 3')
    
    def aboutContributors(self):
        messagebox.showinfo('Contributors', '1.Intishar Alam Misbahul\n2.Google\n3.YouTub\n4.Stackoverflow\n4.Indian guy on YouTube')

    def howToUse(self):
        messagebox.showinfo('How To Use', '1. START - starts the software\n2. UPDATE DB - updates the database of student images\n3. SAVE - saves the attendance file\n4. EXIT - closes the program')

class VideoFeed(tk.Frame):
    
    def __init__(self, parent, controller):
        # inherit __init__ function from tk.Tk class
        tk.Frame.__init__(self, parent)
        
        # bacground set to black
        self.config(background = 'black')
        
        self.controller = controller
        
        # delay per frame
        self.delay = 15
        
        # creates the canvas
        self.canvas = tk.Canvas(self, width = 500, height = 500)
        self.canvas.grid(column=0, row=0, columnspan=2)
        
        # configuring the grid
        self.grid_columnconfigure(0, weight=1, uniform='name')
        self.grid_columnconfigure(1, weight=1, uniform='name')
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # buttons
        self.but1=tk.Button(self,padx=5,pady=5,width=20,height=2,bg='white',fg='black',relief='groove',text='START',font=('helvetica 15 bold'),command= lambda : self.start())
        self.but1.grid(column=0, row=1, padx=15)
        
        self.but2=tk.Button(self,padx=5,pady=5,width=20,height=2,bg='white',fg='black',relief='groove',text='RETURN',font=('helvetica 15 bold'),command= lambda : self.cancel())
        self.but2.grid(column=1, row=1, padx=15)
    
    # starts the camera
    def start(self):
        self.vid = myVideoCapture(0)
        self.myUpdate()
        pass
    
    # closes the window
    def cancel(self):
        self.controller.showFrame(MainScreen)
        self.canvas.delete("all")
        self.vid.close()
        if self.repeatJob is not None:
            self.after_cancel(self.repeatJob)
            self._job = None

    # updates canvas with image
    def myUpdate(self):
        ret, frame = self.vid.getFrame()
        
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = 'nw')
            
        self.repeatJob = self.after(self.delay, self.myUpdate)


    # same menu as before
    def menuBar(self, root):
            
        menubar = tk.Menu(root, bd = 100)
        
        aboutMenu = tk.Menu(menubar, tearoff = 0)
        helpMenu = tk.Menu(menubar, tearoff = 0)
        
        menubar.add_cascade(label="About", menu=aboutMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)
        
        aboutMenu.add_command(label = 'Software', command = self.aboutSoftware)
        aboutMenu.add_command(label = 'Contributors', command = self.aboutContributors)
        
        helpMenu.add_command(label = 'How to Use', command = self.howToUse)
        
        return menubar
    
    def aboutSoftware(self):
        messagebox.showinfo('Software', 'Face Recognition for Attendance v1.0\n Made Using:\n-OpenCV\n-Numpy\n-Tkinter In Python 3')
    
    def aboutContributors(self):
        messagebox.showinfo('Contributors', '1.Intishar Alam Misbahul\n2.Google\n3.YouTub\n4.Stackoverflow\n4.Indian guy on YouTube')

    def howToUse(self):
        messagebox.showinfo('How To Use', '1. START - starts the software\n2. RETURN - closes the program')

class myVideoCapture:
    def __init__(self, videoSource=0):
        # open video source
        self.video = VideoCapture(videoSource)
        
        # initialises classes
        self.faceRecog = FaceRecognition()
        self.attendanceManager = AttendanceDB()
        self.notify = Notify()
        
        # validates camera access
        if not self.video.isOpened():
            self.notify.popUp('Unable to open video source', 3000)

    def getFrame(self):
        # validates if camera was opened or not
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                # flips image
                frame = flip(frame, 1)
                
                # detects face and rturns name of face and location
                result = self.faceRecog.faceDetect(frame)
                
                if result != None:
                    faceLocation, matchName = result
                    # updates student's attendance
                    self.attendanceManager.update_Attendance(matchName)
                    # draws box around face
                    self.faceRecog.drawBox(frame, faceLocation, matchName)
                    # makes a beep sound for notification
                    self.notify.alertSFX()
                
                # returns a boolean flag and current frame converted to BGR
                return (ret, cvtColor(frame, COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release video source when object is destroyed
    def close(self):
        # closes the camera
        if self.video.isOpened():
            self.video.release()

app = App()
app.mainloop()