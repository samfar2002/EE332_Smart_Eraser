import cv2
import random
import numpy as np

def find_candidates(input_frame, size_block, num_candidates):
    image = cv2.imread("original_frames/" + input_frame)
    rows, cols, license = np.shape(image)
    candidates = np.empty([size_block, size_block, license, num_candidates])
    x_max = rows - size_block
    y_max = cols - size_block 

    for i in range(num_candidates):
        x1 = random.randint(0,x_max)
        y1 = random.randint(0,y_max)

        x2 = x1 + size_block
        y2 = y1 + size_block
        current_candidate = image[x1:x2,y1:y2,:]
        candidates[:,:,:,i] = current_candidate
    candidates = candidates.astype(int)
    return candidates 
