import cv2
import os

# decompose_video:
#
# Break video apart into frames that can be manipulated
def decompose_video(file_path, images_folder, frame_no):
    vidcap = cv2.VideoCapture(file_path)
    success,image = vidcap.read()
    count = 0

    # Keep reading images from the video until there are none left
    # to be read
    while success:
        zeros = 4 - len(str(count))
        cv2.imwrite(images_folder + "\\frame" + "0"*zeros + str(count) + '.jpg', image)     
        success,image = vidcap.read()
        count += 1
        


# compose_video:
#
# Puts the frames back into a video and saves
def compose_video(image_folder, file_path, fps):
    # Reads all of the iamges from the folder
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Creates a video writer and writes each frame to the video
    video = cv2.VideoWriter(file_path, 0, fps, (width,height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
