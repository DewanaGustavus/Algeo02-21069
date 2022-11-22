from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilenames
from OpenCV import *
from timeit import default_timer as timer
import os

# BUTTON FUNCTIONS
def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)

def open_img():
    global img
    global imagematrix
    global selection
    x = openfilename()
    imgtemp = Image.open(x)
    imgtemp = imgtemp.resize((256, 256), Image.Resampling.LANCZOS)
    img.paste(imgtemp)

    curpath=os.getcwd()
    curpath=curpath.replace("\\","/")
    
    qq=x.replace(curpath,'')
    new=""
    total=0
    for a in qq:
        if(a=="/"):
            total+=1
    flag=0
    for a in qq:
        if(flag<total):
            if(a=='/'):
                flag+=1
        else:
            new=new+a
    selection.set(new)
    
    canvas.itemconfigure(imgselect,text=selection.get())
    imagematrix = image_to_matrix(x)

def openfilename():
	# open file dialog box to select image
	# The dialogue box has a title "Open"
	filename = filedialog.askopenfilename(title ='Open')
	return filename

def select_file():
	global file_names
	file_names = askopenfilenames(initialdir = "/",
								title = "Select File")

def start_training():
    start=timer()
    global hasiltraining
    global folder_path
    global time_elapsed
    
    imagearray = open_image_folder_to_matrix(folder_path.get()+'/')
    hasiltraining = EigenFunction.training(imagearray)
    end=timer()
    time_elapsed.set("Execution time: " + str(end-start)+ " s") 
    canvas.itemconfigure(timeexec,text=time_elapsed.get())

def recognize():
	global imagematrix
	global hasiltraining
	global folder_path
	global img2
	global resultpath
	closestidx = EigenFunction.indeks_gambar_terdekat(imagematrix, hasiltraining)
	savepath = "img\\closestimage.png"
	if closestidx == -1:
		temp = "Tidak ada gambar yang mirip"
		imgtemp = Image.open("img\\blank.png")
	else:
		files = os.listdir(folder_path.get())
		temp = files[closestidx]
		resultpath=save_image_folder_idx(folder_path.get()+ '/', closestidx, savepath)
		imgtemp = Image.open(savepath)
		imgtemp = imgtemp.resize((256, 256), Image.Resampling.LANCZOS)

	img2.paste(imgtemp)
	closestresult.set("Result : " + temp)
	canvas.itemconfigure(resname,text=closestresult.get())
    

def start():
	global imagematrix	
	global folder_path
	global img2
	global time_elapsed
	global selection
	global closestresult
	global img
	global canvas
	global resname
	global imgselect
	global timeexec
 
	window = Tk()

	window.geometry("972x520")
	window.configure(bg = "#141418")

	canvas = Canvas(
		window,
		bg = "#141418",
		height = 520,
		width = 972,
		bd = 0,
		highlightthickness = 0,
		relief = "ridge"
	)

	canvas.place(x = 0, y = 0)
	image_image_1 = ImageTk.PhotoImage(Image.open("img\\menu.png"))
	image_1 = canvas.create_image(
		486.0,
		260.0,
		image=image_image_1
	)

	# Image showing test image
	img = ImageTk.PhotoImage((Image.open("img\\blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
	image_2 = canvas.create_image(
		472.0,
		299.0,
		image=img
	)

	img2 = ImageTk.PhotoImage((Image.open("img\\blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
	image_3 = canvas.create_image(
		792.0,
		299.0,
		image=img2
	)

	# Button to start training
	button_image_1 = ImageTk.PhotoImage(Image.open("img\\training.png"))
	button_1 = Button(
		image=button_image_1,
		borderwidth=0,
		highlightthickness=0,
		command=start_training
	)
	button_1.place(
		x=46.0,
		y=232.0,
		width=234.0,
		height=58.0
	)

	# Button to find closest image in dataset with input
	button_image_2 = ImageTk.PhotoImage(Image.open("img\\recognize.png"))
	button_2 = Button(
		image=button_image_2,
		borderwidth=0,
		highlightthickness=0,
		command=recognize,
		relief="flat"
	)
	button_2.place(
		x=46.0,
		y=387.0,
		width=234.0,
		height=58.0
	)

	canvas.create_rectangle(
		61.0,
		115.0,
		267.0,
		205.0,
		fill="#141418",
		outline="")

	# Button to choose directory
	button_image_3= ImageTk.PhotoImage(Image.open("img\\buttonicon.png"))
	button_3 = Button(
		image=button_image_3,
		borderwidth=0,
		highlightthickness=0,
		command=browse_button,
		relief="flat"
	)
	button_3.place(
		x=228.0,
		y=150.0,
		width=24.0,
		height=22.0
	)

	canvas.create_rectangle(
		61.0,
		321.0,
		267.0,
		378.0,
		fill="#141418",
		outline="")

	# Button to choose image for recognition
	button_image_4= ImageTk.PhotoImage(Image.open("img\\buttonicon.png"))
	button_4 = Button(
		image=button_image_4,
		borderwidth=0,
		highlightthickness=0,
		command=open_img,
		relief="flat"
	)
	button_4.place(
		x=228.0,
		y=339.0,
		width=24.0,
		height=22.0
	)

	time_elapsed = StringVar()
	time_elapsed.set("Execution time: ")
	timeexec=canvas.create_text(
		61.0,
		218.0,
		anchor="nw",
		text=time_elapsed.get(),
		fill="#FCFCFC",
		font=("Microsoft JhengHei UI Light", 13 * -1)
	)

	# Label to show chosen folder
	folder_path = StringVar()
	folder_path.set("No folder selected.")
	label3 = Label(window, textvariable=folder_path,wraplength=120,height=3,font=("Microsoft JhengHei UI Light", 10),fg="#B7BBC2",bg="#141418")
	label3.grid(column=0, row=0,pady=(130,0),padx=(75,0))

	'''
	canvas.create_text(
		75.0,
		128.0,
		anchor="nw",
		text="No folder selected.",
		fill="#B7BBC2",
		font=("MicrosoftJhengHeiUIRegular", 13 * -1),
		width=0
	)
	'''

	selection=StringVar()
	selection.set("No image selected.")
	imgselect= canvas.create_text(
		75.0,
		332.0,
		anchor="nw",
		text=selection.get(),
		fill="#B7BBC2",
		font=("Microsoft JhengHei UI Regular", 13 * -1)
	)

	canvas.create_text(
		57.0,
		90.0,
		anchor="nw",
		text="Select Dataset",
		fill="#FFFFFF",
		font=("Microsoft JhengHei Bold", 16 * -1)
	)

	closestresult=StringVar()
	closestresult.set("Result : -")
	resname=canvas.create_text(
		670,
		450.0,
		anchor="nw",
		text=closestresult.get(),
		fill="#FFFFFF",
		font=("Microsoft JhengHei Bold", 14 * -1)
	)

	canvas.create_text(
		57.0,
		298.0,
		anchor="nw",
		text="Select Image",
		fill="#FFFFFF",
		font=("Microsoft JhengHei Bold", 16 * -1)
	)
	window.resizable(False, False)
	window.mainloop()

if __name__ == "__main__":
	start()