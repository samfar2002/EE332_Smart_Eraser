import cv2
import numpy as np

def find_pen():
    image = cv2.imread("original_frames\\frame0000.jpg")
    hgt, wid, license = np.shape(image)
    xmin = wid
    ymin = hgt
    xmax = 0
    ymax = 60

    for x in range(wid):
        for y in range(60):
            r = image[y][x][2]
            g = image[y][x][0]
            b = image[y][x][1]
            if (r+g+b) == 0:
                normalized_r = 0
            else:
                normalized_r = r/(r+g+b)
                
            if normalized_r > 0.5:
                if x < xmin:
                    xmin = x
                if y < ymin:
                    ymin = y
                if x > xmax:
                    xmax = x
                if y > ymax:
                    ymax = y
    
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255,255,255))
    cv2.imwrite("result.jpg", image)