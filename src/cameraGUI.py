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
        self.window.geometry("972x520")
        self.window.configure(bg = "#141418")
        self.window.title(window_title)
        
        
        self.video_source = video_source
        self.title = window_title
        self.vid = MyVideoCapture(self.video_source)


        # copas dari gui file
        # Canvas
        self.canvas = tkinter.Canvas(
            window,
            bg = "#141418",
            height = 520,
            width = 972,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = ImageTk.PhotoImage(Image.open("img\\menu.png"))
        self.image_1 = self.canvas.create_image(
            486.0,
            260.0,
            image=self.image_image_1
        )

        # Image showing test image
        self.img = ImageTk.PhotoImage((Image.open("img\\blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
        self.image_2 = self.canvas.create_image(
            472.0,
            299.0,
            image=self.img
        )

        self.img2 = ImageTk.PhotoImage((Image.open("img\\blank.png")).resize((256, 256), Image.Resampling.LANCZOS))
        self.image_3 = self.canvas.create_image(
            792.0,
            299.0,
            image=self.img2
        )

        # Button to start training
        self.button_image_1 = ImageTk.PhotoImage(Image.open("img\\training.png"))
        self.button_1 = tkinter.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_training
        )
        self.button_1.place(
            x=46.0,
            y=232.0,
            width=234.0,
            height=58.0
        )

        # Button to find closest image in dataset with input
        self.button_image_2 = ImageTk.PhotoImage(Image.open("img\\recognize.png"))
        self.button_2 = tkinter.Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.take_photo,
            relief="flat"
        )
        self.button_2.place(
            x=46.0,
            y=387.0,
            width=234.0,
            height=58.0
        )

        self.canvas.create_rectangle(
            61.0,
            115.0,
            267.0,
            205.0,
            fill="#141418",
            outline="")

        # Button to choose directory
        self.button_image_3= ImageTk.PhotoImage(Image.open("img\\buttonicon.png"))
        self.button_3 = tkinter.Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.browse_button,
            relief="flat"
        )
        self.button_3.place(
            x=228.0,
            y=150.0,
            width=24.0,
            height=22.0
        )

        self.canvas.create_rectangle(
            61.0,
            321.0,
            267.0,
            378.0,
            fill="#141418",
            outline="")

        # Button to choose image for recognition
        """
        self.button_image_4= ImageTk.PhotoImage(Image.open("img\\buttonicon.png"))
        self.button_4 = tkinter.Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_img,
            relief="flat"
        )
        self.button_4.place(
            x=228.0,
            y=339.0,
            width=24.0,
            height=22.0
        )
        """
        self.time_elapsed = tkinter.StringVar()
        self.time_elapsed.set("Execution time: ")
        self.timeexec=self.canvas.create_text(
            61.0,
            218.0,
            anchor="nw",
            text=self.time_elapsed.get(),
            fill="#FCFCFC",
            font=("Microsoft JhengHei UI Light", 13 * -1)
        )

        # Label to show chosen folder
        self.folder_path = tkinter.StringVar()
        self.folder_path.set("No folder selected.")
        self.label3 = tkinter.Label(window, textvariable=self.folder_path,wraplength=120,height=3,font=("Microsoft JhengHei UI Light", 10),fg="#B7BBC2",bg="#141418")
        self.label3.grid(column=0, row=0,pady=(130,0),padx=(75,0))

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

        self.selection=tkinter.StringVar()
        self.selection.set("No image selected.")
        self.imgselect=self.canvas.create_text(
            75.0,
            332.0,
            anchor="nw",
            text=self.selection.get(),
            fill="#B7BBC2",
            font=("Microsoft JhengHei UI Regular", 13 * -1)
        )

        self.canvas.create_text(
            57.0,
            90.0,
            anchor="nw",
            text="Select Dataset",
            fill="#FFFFFF",
            font=("Microsoft JhengHei Bold", 16 * -1)
        )

        self.closestresult=tkinter.StringVar()
        self.closestresult.set("Result : -")
        self.resname=self.canvas.create_text(
            670,
            450.0,
            anchor="nw",
            text=self.closestresult.get(),
            fill="#FFFFFF",
            font=("Microsoft JhengHei Bold", 14 * -1)
        )

        self.canvas.create_text(
            57.0,
            298.0,
            anchor="nw",
            text="Select Image",
            fill="#FFFFFF",
            font=("Microsoft JhengHei Bold", 16 * -1)
        )

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 20
        self.update()

        self.window.resizable(False, False)
        self.window.mainloop()
        
    def take_photo(self):
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("img\\camera photo.png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            self.imagematrix = image_to_matrix("img\\camera photo.png")
            closestidx = EigenFunction.indeks_gambar_terdekat(self.imagematrix, self.hasiltraining)
            savepath = "img\\closestimage.png"
            resultpath = save_image_folder_idx(self.folder_path.get()+ '/', closestidx, savepath)
            imgtemp = Image.open(savepath)
            imgtemp = imgtemp.resize((256, 256), Image.Resampling.LANCZOS)
            self.img2.paste(imgtemp)
            
            
            # display closest image name
            temp=""
            total=0
            for a in resultpath:
                if(a=="/"):
                    total+=1
            flag=0
            for a in resultpath:
                if(flag<total):
                    if(a=='/'):
                        flag+=1
                else:
                    temp=temp+a
            self.closestresult.set("Result : " + temp)
            
            
            self.canvas.itemconfigure(self.resname,text=self.closestresult.get())

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            frame = self.vid.rescale_frame(frame)
            imgtemp = PIL.Image.fromarray(frame)
            # self.imgtemp = ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.img.paste(imgtemp)

        self.window.after(self.delay, self.update)
        
    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)

    def openfilename(self):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        filename = filedialog.askopenfilename(title ='Open')
        return filename

    def select_file(self):
        self.file_names = askopenfilenames(initialdir = "/",
                                    title = "Select File")
    
    def start_training(self):
        start = timer()
        imagearray = open_image_folder_to_matrix(self.folder_path.get()+'/')
        self.hasiltraining = EigenFunction.training(imagearray)
        end = timer()
        self.time_elapsed.set("Time elapsed: " + str(end-start)+ " s") 
        self.canvas.itemconfigure(self.timeexec,text=self.time_elapsed.get())

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
    