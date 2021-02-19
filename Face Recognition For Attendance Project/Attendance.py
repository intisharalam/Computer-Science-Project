from datetime import datetime

class Attendance:

    def MarkAttendance(name):
        with open('Face Recognition For Attendance Project\Attendance.csv', 'r+') as f:
            AttendanceList = f.readlines()
            NameList = []
            for line in AttendanceList:
                entry = line.split(',')
                NameList.append(entry[0])
            if name not in NameList:
                now = datetime.now()
                CurrentString = now.strftime('%H:%M')
                f.writelines(f'\n{name},{CurrentString}')