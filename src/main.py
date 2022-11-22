import EigenFunction
import OpenCV
import numpy as np
import math
import cv2 as cv
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilenames
import fileGUI
import cameraGUI

choose=-1
def file_GUI():
    global choose
    choose=1
    window.destroy()
    
def camera_GUI():
    global choose
    choose=2
    window.destroy()

# ROOT
window = Tk()
window.title("Face Recognition Program")
window.configure(bg='white')

# CONTAINER
maincontainer = Frame(window,bg="white")
maincontainer.pack()

# FRAMES

# frame1 -- Title
frame1 = Frame(maincontainer, bg="white")
frame1.grid(column=0, row=0,columnspan=3, sticky="nsw", padx=250, pady=50)

button1= Button(frame1, text="Using file",command=file_GUI)
button1.grid(row=0,column=0,padx=(0,100))

button2= Button(frame1, text="Using camera",command=camera_GUI)
button2.grid(row=0,column=1)
window.mainloop()

if choose==1:
    fileGUI.start()
    
if choose==2:
    cameraGUI.start()