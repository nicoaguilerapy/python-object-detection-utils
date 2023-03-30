import cv2
import numpy as np
from pynput.keyboard import Key, Controller
from win32api import GetSystemMetrics
import os
import imgtoxml as ix

#INSTRUCCIONES
# 1. Cambiar el COUNT a la cantidad de imagenes que ya se tienen en el directorio
# 2. Primeros 2 click del mouse son para recortar la imagen (OBLIGATORIO)
# 3. Siguientes 2 click son para marcar la placa (OBLIGATORIO)
# 4. Presionar cualquier tecla para continuar (menos Q en miniscula, que es para salir)

posList = []
def onMouse(event, x, y, flags, param):
   global posList
   if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        if len(posList) == 2:
            keyboard = Controller()
            key = "0"
            keyboard.press(key)
            keyboard.release(key)

COUNT = 279 #contador inicial en CarsX.png y CarsX.xml
PATH = "training_images"
files = os.listdir(PATH)

for file in files:
    img=cv2.imread("{}/{}".format(PATH,file))
    dimensions = img.shape

    #verifica si una de las dimensiones es mayor a 500px, para hacer un reajuste proporcional a ese tamanho
    scale_percent = 0
    if dimensions [0] > 500:
        scale_percent = 50000/dimensions[0]
    elif dimensions [1] > 500:
        scale_percent = 50000/dimensions[1]
        

    #redumensiona porcentualmente, de lo contrario usa una copia de la misma imagen
    if scale_percent > 0:
        width = int(dimensions[1] * scale_percent / 100)
        height = int(dimensions[0] * scale_percent / 100)
        dim = (width, height)
        new_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    else:
        new_img = img.copy()
    

    winname = PATH
    #centro de la imgen en el centro de la pantalla
    screenX = int(GetSystemMetrics(0)/2)-int(width/2)
    screenY = int(GetSystemMetrics(1)/2)-int(height/2)
    cv2.namedWindow(PATH) 
    cv2.moveWindow(winname, screenX, screenY) 
    cv2.imshow(winname, new_img)
    cv2.setMouseCallback(PATH, onMouse)
    cv2.waitKey(0)
    cv2.destroyWindow(PATH)
    #recortar la imagen en 2 puntos
    x, y = posList[0]
    width, height = posList[1]
    new_imgori_cut = new_img[y:height, x:width]
    posList.clear()
    
    #mostrar la imagen recortada
    cv2.namedWindow(PATH) 
    cv2.moveWindow(winname, screenX, screenY) 
    cv2.imshow(winname, new_imgori_cut)
    cv2.setMouseCallback(PATH, onMouse)
    cv2.waitKey(0)
    cv2.destroyWindow(PATH)
    
    #mostrar la imagen recortada con el rectangulo de la placa
    color = (255, 0, 0)
    rec = cv2.rectangle(new_imgori_cut.copy(), posList[0], posList[1], color, 2)
    cv2.namedWindow(winname) 
    cv2.moveWindow(winname, screenX, screenY) 
    cv2.imshow(winname, rec)
    cv2.waitKey(0)

    #Se crea el archivo xml
    xml_file = ix.DATAtoXML()
    xml_file.filename = "Cars{}.png".format(COUNT)
    xml_file.width = new_img.shape[1]
    xml_file.height = new_img.shape[0]
    xml_file.xmin = posList[0][0]
    xml_file.ymin = posList[0][1]
    xml_file.xmax = posList[1][0]
    xml_file.ymax = posList[1][1]
    xml_file.setXML()
    xml_file.save(COUNT)
    
    cv2.imwrite("result/Cars{}.png".format(COUNT), new_imgori_cut)
    COUNT = COUNT + 1
    posList.clear()
