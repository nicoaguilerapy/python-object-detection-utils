import cv2
import os
import imgtoxml as ix
import xml.etree.ElementTree as ET


PATH = "result"
files = os.listdir(PATH)

for file in files:
    if not file.endswith(".png"):
        continue
    img=cv2.imread("{}/{}".format(PATH,file))
    dimensions = img.shape
    
    # if dimensions[0] > 500 or dimensions[1] > 500:
    #     print(file, dimensions)
    # else:
    #     continue

    # #verifica si una de las dimensiones es mayor a 500px, para hacer un reajuste proporcional a ese tamanho

    # scale_percent = 0
    # if dimensions [0] > 500:    
    #     scale_percent = 50000/dimensions[0]
    # elif dimensions [1] > 500:
    #     scale_percent = 50000/dimensions[1]

    # #redumensiona porcentualmente, de lo contrario usa una copia de la misma imagen
    # if scale_percent > 0:
    #     width = int(dimensions[1] * scale_percent / 100)
    #     height = int(dimensions[0] * scale_percent / 100)
    #     dim = (width, height)
    #     new_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # else:
    #     new_img = img.copy()
    
    # print("ANTERIOR: ", file, dimensions)
    # print("SCALA: ", scale_percent)
    # print("NUEVO: ", file, new_img.shape)
    #remover letras del nombre de la imagen y dejar solo los numeros
    COUNT = file.replace("Cars", "").replace(".png", "")

    tree = ET.parse('{}/Cars{}.xml'.format(PATH, COUNT))
    root = tree.getroot()

    xml_file = ix.DATAtoXML()
    xml_file.filename = "Cars{}.png".format(COUNT)
    xml_file.width = img.shape[1]
    xml_file.height = img.shape[0]
    xml_file.xmin = root[4][5][0].text
    xml_file.ymin = root[4][5][1].text
    xml_file.xmax = root[4][5][2].text
    xml_file.ymax = root[4][5][3].text
    xml_file.setXML()
    xml_file.save(COUNT)

