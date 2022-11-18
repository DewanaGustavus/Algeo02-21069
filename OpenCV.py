import EigenFunction
import cv2 as cv
import numpy as np
import os
import shutil
from PIL import Image
import numpy as np

def image_to_matrix(imagepath):
    im = Image.open(imagepath)
    sqrWidth = np.ceil(np.sqrt(im.size[0]*im.size[1])).astype(int)
    im_resize = im.resize((sqrWidth, sqrWidth))
    im_resize.save("tmpoutput.png")
    image = cv.imread("tmpoutput.png", 0) # 0 for black and white mode
    os.remove("tmpoutput.png")
    return image

def matrix_to_image(matrix, savepath):
    cv.imwrite(savepath, matrix)
    
def open_image_folder_to_matrix(folderpath):
    files = os.listdir(folderpath)
    length = len(files)
    imagearray = []
    for i in range(length):
        imagepath = folderpath + files[i]
        matrix = image_to_matrix(imagepath)
        imagearray.append(matrix)
    return imagearray

def save_image_folder_idx(folderpath, idx, savepath):
    files = os.listdir(folderpath)
    imagepath = folderpath + files[idx]
    shutil.copyfile(imagepath, savepath)
    
def camera():
    vid = cv.VideoCapture(0)
    while(True):
        ret, frame = vid.read()
        cv.imshow("Camera", frame) 
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        if cv.waitKey(1) & 0xFF == ord('w'):
            cv.imwrite('opencv'+'.png', frame)

    vid.release()
    cv.destroyAllWindows()
    
if __name__ == "__main__":
    folderpath = "anyatest\\"
    image1path = folderpath + "anya 1.png"
    
    # tes training
    imagearray = open_image_folder_to_matrix(folderpath)
    K, C_aksen, psi, Omega = EigenFunction.training(imagearray)
    imagematrix = image_to_matrix(image1path)
    closestidx = EigenFunction.indeks_gambar_terdekat(imagematrix, K, C_aksen, psi, Omega)
    save_image_folder_idx(folderpath, closestidx, "closestanya.png")
    
    