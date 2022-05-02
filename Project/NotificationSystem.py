from pygame import mixer
from pathlib import Path
from tkinter import Tk, Label, Button

class Notify:
    
    PATH = PATH = Path(__file__).resolve().parent  # path to parent folder
    
    def __init__(self, src=PATH, window_title='PopUp'):
        self.src = src / 'beep.wav' # path to sound file
        self.win_title = window_title
    
    def alertSFX(self):
        mixer.init()
        alert=mixer.Sound(self.src)
        alert.play()

    def popUp(self, msg='TEST TEXT', delay=5000):
        popup = Tk()
        popup.title(self.win_title)
        label = Label(popup, text=msg,font=("Courier", 13))
        label.pack(side='top', fill='x', pady=10)

        popup.after(delay, lambda: popup.destroy())
        popup.mainloop()