
from tqdm import *

video_path = 'video1.mp4'
video_out = video_path[:-4] + '_detected' + video_path[-4:]
video_reader = cv2.VideoCapture(video_path)

nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

video_writer = cv2.VideoWriter(video_out,
                       cv2.VideoWriter_fourcc(*'MPEG'), 
                       50.0, 
                       (frame_w, frame_h))

for i in tqdm(range(nb_frames)):
    _, image = video_reader.read()
    
    boxes = mi_yolo.predict(image)
    image = draw_boxes(image, boxes, labels)

    video_writer.write(np.uint8(image))

video_reader.release()
video_writer.release()

win_name = 'Lego detection'
cv2.namedWindow(win_name)

video_reader = cv2.VideoCapture(0)

while True:
    _, image = video_reader.read()
    
    boxes = mi_yolo.predict(image)
    image = draw_boxes(image, boxes, labels)

    cv2.imshow(win_name, image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
video_reader.release()