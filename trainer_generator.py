import cv2
import numpy as np
from pynput.keyboard import Key, Controller
from win32api import GetSystemMetrics
import os
import imgtoxml as ix

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

COUNT = 0
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
    
    new_imgOri = new_img.copy()

    winname = PATH
    #centro de la imgen en el centro de la pantalla
    screenX = int(GetSystemMetrics(0)/2)-int(width/2)
    screenY = int(GetSystemMetrics(1)/2)-int(height/2)
    cv2.namedWindow(winname) 
    cv2.moveWindow(winname, screenX, screenY) 
    cv2.imshow(winname, new_img)

    cv2.setMouseCallback(PATH, onMouse)
    cv2.waitKey(0)
    cv2.destroyWindow(PATH)

    color = (255, 0, 0)
    rec = cv2.rectangle(new_img.copy(), posList[0], posList[1], color, 2)
    cv2.namedWindow(winname) 
    cv2.moveWindow(winname, screenX, screenY) 
    cv2.imshow(winname, rec)
    cv2.waitKey(0)

    #inicio y fin del corte
    x, y = posList[0]
    width, height = posList[1]
    crop_img = img[y:height, x:width]
    print(y,height, x,width)

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
    
    cv2.imwrite("result/Cars{}.png".format(COUNT), new_imgOri)
    COUNT = COUNT + 1
    posList.clear()
