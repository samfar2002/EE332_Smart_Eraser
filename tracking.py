import cv2
import numpy as np
import os

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
    
    return (xmin, ymin, xmax, ymax)

def find_pen_ssd(first_coords):
    x1, y1, x2, y2 = first_coords
    images = [img for img in os.listdir('original_frames')]
    images = [cv2.imread('original_frames\\' + image) for image in images]

    ref_image = images[0][y1:y2, x1:x2]
    ref_image1 = images[0][y1:y2, x1:x2]
    x_coords = []
    x_coords.append(int(np.round((x1+x2)/2)))
    i = 1
    for image in images[1:]:
        ssd_min = 100000000
        for u in range(-5,6):
            for v in range(-5,6):
                new_image = image[y1+v:y2+v, x1+u:x2+u]
                ssd = np.sum((ref_image[:,:,:]-new_image[:,:,:])**2) + np.sum((ref_image1[:,:,:]-new_image[:,:,:])**2)
                if ssd < ssd_min:
                    ssd_min = ssd
                    ufin = u
                    vfin = v
        x1 = x1 + ufin
        x2 = x2 + ufin
        y1 = y1 + vfin
        y2 = y2 + vfin
        x_coords.append(int(np.round((x1+x2)/2)))
        ref_image = image[y1:y2, x1:x2]
        cv2.rectangle(image,(x1, y1), (x2, y2), (255,255,255))
        zeros = 4 - len(str(i))
        cv2.imwrite('original_frames\\frame' + "0"*zeros + str(i) + '.jpg', image)
        i += 1
    
    return x_coords


def find_textures_to_replace(input_frame, x_cord):
    image = cv2.imread("original_frames\\" + input_frame)
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
