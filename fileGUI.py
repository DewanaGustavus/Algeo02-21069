from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilenames
from OpenCV import *
from timeit import default_timer as timer

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

	x = openfilename()
	imgtemp = Image.open(x)
	imgtemp = imgtemp.resize((256, 256), Image.Resampling.LANCZOS)
	img.paste(imgtemp)

	imagematrix = image_to_matrix(x)

def openfilename():
	# open file dialog box to select image
	# The dialogue box has a title "Open"
	filename = filedialog.askopenfilename(title ='"pen')
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
    time_elapsed.set("Time elapsed: " + str(end-start)+ " s") 

def recognize():
    global imagematrix
    global hasiltraining
    global folder_path
    global img2
    closestidx = EigenFunction.indeks_gambar_terdekat(imagematrix, hasiltraining)
    savepath = "closestimage.png"
    save_image_folder_idx(folder_path.get()+ '/', closestidx, savepath)
    imgtemp = Image.open(savepath)
    imgtemp = imgtemp.resize((256, 256), Image.Resampling.LANCZOS)
    img2.paste(imgtemp)
    
def start():
	global imagematrix
	global hasiltraining
	global folder_path
	global img2
	global hasiltraining
	global time_elapsed
	global file_names
	global img
 
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
	frame1.grid(column=0, row=0,columnspan=3, sticky="nsw", padx=350, pady=50)

	# framecontain - Frame under title
	framecontain = Frame(maincontainer,bg='white')
	framecontain.grid(column=0, row=1, sticky='wns', pady=10)

	# frame2 -- Choosing dataset & image
	frame2 = Frame(framecontain, padx=10, bg="white")
	frame2.grid(column=0, row=0,padx=10)

	# frame 3 -- Displaying chosen image
	frame3 = Frame(framecontain, bg="white")
	frame3.grid(column=1, row=0,padx=50)

	# frame 4 -- Displaying result
	frame4 = Frame(framecontain, bg="white")
	frame4.grid(column=2, row=0,padx=50)

	# COMPONENTS

	judul2 = Label(frame1, text="Face Recognition", font=("Microsoft JhengHei UI Light", 25), bg="white")
	judul2.grid(column=0, row=0)

	label1 = Label(frame2, text="Insert Your Dataset", font=("Microsoft JhengHei UI Light", 15), bg="white")
	label1.grid(column=0, row=0,pady=(0,10))

	# Label to show chosen folder
	folder_path = StringVar()
	folder_path.set("No folder chosen")
	lbl1 = Label(frame2,textvariable=folder_path,wraplength=170,height=5, bg="white")
	lbl1.grid(row=2, column=0)

	# Button to choose directory
	button2 = Button(frame2,text="Browse", command=browse_button)
	button2.grid(row=1, column=0)

	label2 = Label(frame2, text="Insert Your Image", font=("Microsoft JhengHei UI Light", 15), bg="white")
	label2.grid(column=0, row=3)

	# Button to choose image for recognition
	button3 = Button(frame2,text="Browse", command=open_img)
	button3.grid(row=4, column=0,pady=(0,120))

	button4= Button(frame2, text="Start training",command=start_training)
	button4.grid(row=5,column=0)

	time_elapsed = StringVar()
	time_elapsed.set("Time elapsed :")
	label3 = Label(frame2, textvariable=time_elapsed, font=("Microsoft JhengHei UI Light", 10), bg="white")
	label3.grid(column=0, row=6)

	button5= Button(frame2, text="Recognize",command=recognize)
	button5.grid(row=7,column=0)

	label3 = Label(frame3, text="Test Image", font=("Microsoft JhengHei UI Light", 13), bg="white")
	label3.grid(column=0, row=0)

	# Image showing test image
	img = ImageTk.PhotoImage((Image.open("blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
	imgLabel = Label(frame3, image=img)
	imgLabel.grid(column=0, row=1,pady=(10,0))

	label4 = Label(frame4, text="Closest Result", font=("Microsoft JhengHei UI Light", 13), bg="white")
	label4.grid(column=0, row=0)

	# Image showing closest image
	img2 = ImageTk.PhotoImage((Image.open("blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
	img2Label = Label(frame4, image=img2)
	img2Label.grid(column=0, row=1,pady=(10,0))

	window.mainloop()

if __name__ == "__main__":
    start()