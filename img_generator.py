import numpy as np
import cv2

# path del video
video = '2.mp4'

frames = []
PATH = "training_images"


#recorre a video frame a frame con las funciones de opencv y las flechas de numpy
def detectCars(filename):
    vc = cv2.VideoCapture(filename)
    i = 13
    #proceso de cargar la lista de frames
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        
        rval, frame = vc.read()
        if rval:
            cv2.imshow('frame', frame) 
            key = cv2.waitKey(0)
            if key == 103:
                i = i + 1
                cv2.imwrite("{}/frame{}.jpg".format(PATH, i), frame)
            elif key == 113:
                cv2.destroyAllWindows()
                break
            else:
                pass
        
        else:
            cv2.destroyAllWindows()
            
    vc.release()


detectCars(video)