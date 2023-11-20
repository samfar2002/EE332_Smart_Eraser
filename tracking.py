import cv2
import numpy as np

def find_pen():
    image = cv2.imread("original_frames\\frame0000.jpg")
    hgt, wid, license = np.shape(image)
    xmin = wid
    ymin = hgt
    xmax = 0
    ymax = 0

    for x in range(wid):
        for y in range(60):
            if image[x][y][2]