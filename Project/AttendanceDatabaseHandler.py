from datetime import datetime
from pathlib import Path
from NotificationSystem import Notify

class AttendanceDB:
    
    now = datetime.now()
    curTime = now.strftime('%H:%M') # gets current time in 24hr format [00Hr:00min]
    curDate = now.strftime('%d-%a-%Y')  # gets current date in the format [day-month-year]
    
    PATH = Path(__file__).resolve().parent  # path to parent folder
    
    def __init__(self):
        self.src = self.PATH / 'Attendance.csv' # path to attendance file
        self.dst = self.PATH / 'SavedAttendance' / f'Attendance-{self.curDate}.csv' # path for SavedAttendance directory
        
        self.notify = Notify()
    
    def update_Attendance(self, name):
        if self.src.exists():   # checks if attendance.csv file exists
            with open(self.src, 'r+') as f:
                fileData = f.readlines()    # loads content of the file
                nameList = []   # array for names in the file

                for line in fileData:   # iterates through each line in the file
                    lineContents = line.split(',')  # splits contents seperated by ',' in each line
                    nameList.append(lineContents[0])    # appends the first part of each line [name,time,date]
                
                if name not in nameList:    # checks if name passed into the function has already been entered or not
                    f.writelines(f'{name},{self.curTime},{self.curDate}\n') # writes entry for that name if not already entered
            f.close()
        else:
            with open(self.src, 'w') as f:  # creats the file if it does not exist
                f.writelines(f'{name},{self.curTime},{self.curDate}\n') # enters entry for the name
            f.close()

    def save_Attendance(self):
        if self.src.exists():   # checks if attendance.csv exists for copy
            with open(self.dst,'w') as f:   # creates an empty file for copy
                pass
            f.close()
            
            with open(self.src,'r') as origFile, open(self.dst,'a') as copyFile:    # opens both original and file to be copied to
                copyFile.writelines(origFile.readlines())   # copies data from original to the other
            origFile.close()
            copyFile.close()
            
            self.notify.popUp(f'\nSaved as: \nAttendance-{self.curDate}.csv\n\n# Note: Copies are replaced')
        else:
            self.notify.popUp('No file to save!', 2000)