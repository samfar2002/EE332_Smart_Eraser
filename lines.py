import cv2
import numpy as np

def find_dark(frame):
    image = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
    height, width = np.shape(image)
    for y in range(height):
        for x in range(width):
            if image[y,x] > 80:
                image[y,x] = 0
            else:
                image[y,x] = 255
    
    cv2.imwrite("test_find.jpg", image)

def find_lines(frame):
    image = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
    height, width = np.shape(image)
    passing_cols = []
    for x in range(59, 290):
        sum = 0
        for y in range(130, 200):
            sum += image[y,x]
        
        if sum/255 < 2:
            passing_cols.append(x)
    
    new_image = cv2.imread("finaltexture.jpg")
    new_image_2 = cv2.imread("finaltexture.jpg")
    count = 0
    lines = []
    for index, col in enumerate(passing_cols):
        if index == 0:
            cv2.line(new_image, (col,0), (col, height-1), (0, 0, 255))
            count += 1
            lines.append(col)
        if index>0 and passing_cols[index-1] != col-1:
            cv2.line(new_image, (col,0), (col, height-1), (0, 0, 255))
            count += 1
            lines.append(col)

    text_lines = []
    for index in range(1,len(lines)):
        text = int(np.round(lines[index-1] + lines[index])/2)
        text_lines.append(text)
        cv2.line(new_image_2, (text,0), (text, height-1), (255, 0, 0))
        
        
    cv2.line(new_image, (58,0), (58, height-1), (0, 255, 0))
    cv2.line(new_image, (291,0), (291, height-1), (0, 255, 0))
    cv2.line(new_image_2, (58,0), (58, height-1), (0, 255, 0))
    cv2.line(new_image_2, (291,0), (291, height-1), (0, 255, 0))
    cv2.imwrite("in_between.jpg", new_image)
    cv2.imwrite("over_text.jpg", new_image_2)

    return text_lines