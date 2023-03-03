import numpy as np
import cv2

# path del video
video = 'carv.mp4'

frames = []
PATH = "training_images"

def detectCars(filename):
    print("CARGANDO FRAMES, ESTO PUEDE DEMORAR MUCHOS SEGUNDOS...")
    vc = cv2.VideoCapture(filename)
    c = 0
    
    #obtiene la cantidad de frames del video
    frame_count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

    print("CANTIDAD DE FRAMES: ", frame_count)
 

    #proceso de cargar la lista de frames
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        
        print("PROCESO: {}".format(int((c/frame_count)*100)), flush=True, end="\r")
        rval, frame = vc.read()
        if rval:
            c = c + 1
            frames.append(frame)
    

#muestra cada frame, con S para siguiente y A para anterior, ESC para salir, G para guardar
def show_frame(i):
    cv2.imshow('frame', frames[i]) 
    key = cv2.waitKey(0)
    print(key)
    if i < len(frames) - 1:
        if key == 115:
            show_frame(i + 1)
        elif key == 97:
            show_frame(i - 1)
        elif key == 103:
            cv2.imwrite("{}/frame{}.jpg".format(PATH, i), frames[i])
            print("frame{}.jpg".format(i))
            show_frame(i+1)
        elif key == 27:
            cv2.destroyAllWindows()
        else:
            show_frame(i)
    else:
        cv2.destroyAllWindows()



    
    



detectCars(video)
show_frame(0)