from tkinter import *
from tkinter.ttk import *
from time import strftime

root = Tk()
root.title("Digital Clock")

def time():
    string = strftime('%H:%M:%S %p \n %D')
    label.config(text = string)
    label.after(1000, time)

label = Label(root, font = ('calibri', 40, 'bold'), background = 'black', foreground = 'cyan')
label.pack(anchor = 'center')
time()

mainloop()