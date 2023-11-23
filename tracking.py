import cv2
import numpy as np

def find_pen(input_frame):
    image = cv2.imread("original_frames\\" + input_frame)
    hgt, wid, license = np.shape(image)
    xmin = wid
    ymin = hgt
    xmax = 0
    ymax = 0

    for x in range(wid):
        for y in range(60):
            r = int(image[y][x][2])
            g = int(image[y][x][0])
            b = int(image[y][x][1])
            if (r+g+b) == 0:
                normalized_r = 0
            else:
                normalized_r = r/(r+g+b)
                
            if normalized_r > 0.7:
                if x < xmin:
                    xmin = x
                if y < ymin:
                    ymin = y
                if x > xmax:
                    xmax = x
                if y > ymax:
                    ymax = y
    
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255,255,255))
    cv2.imwrite("original_frames\\" + input_frame, image)

    return int((xmin + xmax)/2)

def find_textures_to_replace(image, x_cord):
    image = cv2.imread("original_frames/" + input_frame)
    rows, cols, license = np.shape(image)
    y_values = np.array([])
    for y in range(60,rows):
        r = image[y,x_cord,0]
        g = image[y,x_cord,1]
        b = image[y,x_cord,2]
        
        if (r+g+b) == 0:
            normalized_r = 0
        else:
            normalized_r = r/(r+g+b)
        
        if normalized_r > 0.7:
            y_values = np.append(y_values,y)
            
    return y_values
