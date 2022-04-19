from tkinter import *

rootTxt = Tk()
rootTxt.geometry('200x100')

Console = Text(rootTxt)
Console.tag_configure('center', justify='center')
Console.insert('1.0', 'text')
Console.tag_add('center', '1.0', 'end')
Console.pack()

def write(*message, end='\n', sep=' '):
    text = ''
    for item in message:
        text += '{}'.format(item)
        text += sep
    text += end
    Console.insert(INSERT, text)

write('hello')

rootTxt.mainloop()

