import cv2
import numpy as np
import os


# find_pen:
#
# Finds the pen in the first frame and returns the max and min
# x and y values of it to become the bounding box to track for
# the subsequent frames
def find_pen(input_frame):
    # Read image and initalize max and min values
    image = cv2.imread("original_frames\\" + input_frame)
    hgt, wid, license = np.shape(image)
    xmin = wid
    ymin = hgt
    xmax = 0
    ymax = 0

    # For each pixel, make sure that the normalized red value is
    # large enough, (since the pen and text are the largest red values)
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
                # If so, and it is outside the bounds of the previous mins 
                # and max, reassign those values
                if x < xmin:
                    xmin = x
                if y < ymin:
                    ymin = y
                if x > xmax:
                    xmax = x
                if y > ymax:
                    ymax = y
    
    # Draw a rectangle around the pen and save the image
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255,255,255))
    cv2.imwrite("original_frames\\" + input_frame, image)
    
    # Return location of the bounding box to track
    return (xmin, ymin, xmax, ymax)



# find_pen_ssd:
#
# Tracks the pen for each frame, draws in a rectangle for where the pen is
# and returns the location as a list
def find_pen_ssd(first_coords):
    # Extracts beginning bounding box
    x1, y1, x2, y2 = first_coords
    # Reads images
    images = [img for img in os.listdir('original_frames')]
    images = [cv2.imread('original_frames\\' + image) for image in images]

    # Finds reference image for tracking
    ref_image = images[0][y1:y2, x1:x2]
    ref_image1 = images[0][y1:y2, x1:x2]
    x_coords = []
    x_coords.append(int(np.round((x1+x2)/2)))
    i = 1
    # For each frame, it finds the pen using ssd comparison to the
    # preview reference value and local exhaustive search since the pen
    # is not moving too quickly
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
        # Reassigns reference for next iteration
        x1 = x1 + ufin
        x2 = x2 + ufin
        y1 = y1 + vfin
        y2 = y2 + vfin
        # Saves the coordinate into the list
        x_coords.append(int(np.round((x1+x2)/2)))
        ref_image = image[y1:y2, x1:x2]
        # Draws the rectangle onto the image and saves
        cv2.rectangle(image,(x1, y1), (x2, y2), (255,255,255))
        zeros = 4 - len(str(i))
        cv2.imwrite('original_frames\\frame' + "0"*zeros + str(i) + '.jpg', image)
        i += 1
    
    # Returns the list of x coordinates of the center of the box in each frame
    return x_coords
