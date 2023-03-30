import cv2
import os
PATH = "training_images"

#recorrer la carpeta con las imagenes y hacer el espejo en el eje x
def mirrorImages():
    for i, file in enumerate(os.listdir(PATH)):
        img = cv2.imread(PATH+"/"+file)
        img = cv2.flip(img, 1)
        cv2.imwrite(PATH+"/"+file, img)

mirrorImages()