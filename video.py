import cv2
import os

def decomposeVideo(file_path, images_folder, frame_no):
    vidcap = cv2.VideoCapture(file_path)
    success,image = vidcap.read()
    count = 0

    while success:
        zeros = 4 - len(str(count))
        cv2.imwrite(images_folder + "\\frame" + "0"*zeros + str(count) + '.jpg', image)     
        success,image = vidcap.read()
        count += 1
        

def composeVideo(image_folder, file_path, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(file_path, 0, fps, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
