from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilenames
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from OpenCV import *
from timeit import default_timer as timer


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.configure(bg='white')
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)


        # copas dari gui file
        # CONTAINER
        self.maincontainer = tkinter.Frame(window,bg="white")
        self.maincontainer.pack()

        # FRAMES
        # frame1 -- Title
        self.frame1 = tkinter.Frame(self.maincontainer, bg="white")
        self.frame1.grid(column=0, row=0,columnspan=3, sticky="nsw", padx=350, pady=50)
        # framecontain - Frame under title
        self.framecontain = tkinter.Frame(self.maincontainer,bg='white')
        self.framecontain.grid(column=0, row=1, sticky='wns', pady=10)
        # frame2 -- Choosing dataset & image
        self.frame2 = tkinter.Frame(self.framecontain, padx=10, bg="white")
        self.frame2.grid(column=0, row=0,padx=10)
        # frame 3 -- Displaying chosen image
        self.frame3 = tkinter.Frame(self.framecontain, bg="white")
        self.frame3.grid(column=1, row=0,padx=50)
        # frame 4 -- Displaying result
        self.frame4 = tkinter.Frame(self.framecontain, bg="white")
        self.frame4.grid(column=2, row=0,padx=50)

        # COMPONENTS
        self.judul2 = tkinter.Label(self.frame1, text="Face Recognition", font=("Microsoft JhengHei UI Light", 25), bg="white")
        self.judul2.grid(column=0, row=0)
        self.label1 = tkinter.Label(self.frame2, text="Insert Your Dataset", font=("Microsoft JhengHei UI Light", 15), bg="white")
        self.label1.grid(column=0, row=0,pady=(0,10))

        # Label to show chosen folder
        self.folder_path = tkinter.StringVar()
        self.folder_path.set("No folder chosen")
        self.lbl1 = tkinter.Label(self.frame2,textvariable=self.folder_path,wraplength=170,height=5, bg="white")
        self.lbl1.grid(row=2, column=0)

        # Button to choose directory
        self.button2 = tkinter.Button(self.frame2,text="Browse", command=self.browse_button)
        self.button2.grid(row=1, column=0)
        self.label2 = tkinter.Label(self.frame2, text="Insert Your Image", font=("Microsoft JhengHei UI Light", 15), bg="white")
        self.label2.grid(column=0, row=3)

        # Button to choose image for recognition (moved to update function)

        # Image showing test image
        self.img = ImageTk.PhotoImage((Image.open("blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
        self.imgLabel = tkinter.Label(self.frame3, image=self.img)
        self.imgLabel.grid(column=0, row=1,pady=(10,0))
        self.label4 = tkinter.Label(self.frame4, text="Closest Result", font=("Microsoft JhengHei UI Light", 13), bg="white")
        self.label4.grid(column=0, row=0)
        
        # Image showing closest image
        self.img2 = ImageTk.PhotoImage((Image.open("blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
        self.img2Label = tkinter.Label(self.frame4, image=self.img2)
        self.img2Label.grid(column=0, row=1,pady=(10,0))

        # Button that lets the user take a snapshot and do face recognition
        self.btn_snapshot=tkinter.Button(self.window, text="Snapshot", width=50, command=self.take_photo)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        
        # Button that lets the user to start training
        self.button4= tkinter.Button(self.frame2, text="Start training",command=self.start_training)
        self.button4.grid(row=5,column=0)
        self.time_elapsed = tkinter.StringVar()
        self.time_elapsed.set("Time elapsed :")
        self.label3 = tkinter.Label(self.frame2, textvariable=self.time_elapsed, font=("Microsoft JhengHei UI Light", 10), bg="white")
        self.label3.grid(column=0, row=6)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()
        
    def take_photo(self):
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("camera photo" + ".png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            self.imagematrix = image_to_matrix("camera photo.png")
            closestidx = EigenFunction.indeks_gambar_terdekat(self.imagematrix, self.hasiltraining)
            savepath = "closestimage.png"
            save_image_folder_idx(self.folder_path.get()+ '/', closestidx, savepath)
            imgtemp = Image.open(savepath)
            imgtemp = imgtemp.resize((256, 256), Image.Resampling.LANCZOS)
            self.img2.paste(imgtemp)

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            frame = self.vid.rescale_frame(frame)
            self.img = ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.imgLabel = tkinter.Label(self.frame3, image=self.img)
            self.imgLabel.grid(column=0, row=1,pady=(10,0))
            self.label4 = tkinter.Label(self.frame4, text="Closest Result", font=("Microsoft JhengHei UI Light", 13), bg="white")
            self.label4.grid(column=0, row=0)

        self.window.after(self.delay, self.update)
        
    # BUTTON FUNCTIONS
    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)

    def openfilename(self):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        filename = filedialog.askopenfilename(title ='"pen')
        return filename

    def select_file(self):
        global file_names
        file_names = askopenfilenames(initialdir = "/",
                                    title = "Select File")
    def start_training(self):
        start=timer()
        imagearray = open_image_folder_to_matrix(self.folder_path.get()+'/')
        self.hasiltraining = EigenFunction.training(imagearray)
        end=timer()
        self.time_elapsed.set("Time elapsed: " + str(end-start)+ " s") 

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
        
    def rescale_frame(self, frame):    # works for image, video, live video
        dimensions = (256, 256)
        return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def start():
    App(tkinter.Tk(), "Face Recognition with Camera")


if __name__ == "__main__":
    start()