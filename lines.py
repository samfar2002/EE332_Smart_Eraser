import cv2
import numpy as np

# find_dark:
#
# Saves an image of the black and white results of thresholding
# the image to find the text
def find_dark(frame):
    # Read image and get shape
    image = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
    height, width = np.shape(image)

    # For each pixel, test whether is is dark enough to be considered text
    # and rewrite value
    for y in range(height):
        for x in range(width):
            if image[y,x] > 80:
                image[y,x] = 0
            else:
                image[y,x] = 255
    
    # Save image
    cv2.imwrite("test_find.jpg", image)



# find_lines:
#
# Returns the columns of the pixels where the lines of
# text are centered
def find_lines(frame):
    # Read image and image size
    image = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
    height, width = np.shape(image)

    # For each column of the image, test whether the total number
    # of white pixels is small enough to be considered as a space between the text
    passing_cols = []
    for x in range(59, 290):
        sum = 0
        for y in range(130, 200):
            sum += image[y,x]
        
        # If so, append to the list to save
        if sum/255 < 2:
            passing_cols.append(x)
    
    # Read the image again to save progress picture
    new_image = cv2.imread("finaltexture.jpg")
    new_image_2 = cv2.imread("finaltexture.jpg")

    # For each passing column, make sure that it is the only adjacent column.
    count = 0
    lines = []
    for index, col in enumerate(passing_cols):
        if index == 0:
            cv2.line(new_image, (col,0), (col, height-1), (0, 0, 255))
            count += 1
            lines.append(col)
        if index>0 and passing_cols[index-1] != col-1:
            # If so, draw in the line for the column between the lines of text
            cv2.line(new_image, (col,0), (col, height-1), (0, 0, 255))
            count += 1
            lines.append(col)

    # For each of the passing columms, average with the next one (to find where the
    # line of text is centered) and then draw in a line
    text_lines = []
    for index in range(1,len(lines)):
        text = int(np.round(lines[index-1] + lines[index])/2)
        text_lines.append(text)
        cv2.line(new_image_2, (text,0), (text, height-1), (255, 0, 0))

    # Extra lines just for aesthetic purposes of showing resutls
    cv2.line(new_image, (58,0), (58, height-1), (0, 255, 0))
    cv2.line(new_image, (291,0), (291, height-1), (0, 255, 0))
    cv2.line(new_image_2, (58,0), (58, height-1), (0, 255, 0))
    cv2.line(new_image_2, (291,0), (291, height-1), (0, 255, 0))
    cv2.imwrite("in_between.jpg", new_image)
    cv2.imwrite("over_text.jpg", new_image_2)

    # Return the final list of the columns where the text lines are
    return text_lines