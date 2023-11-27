import cv2
import random
import numpy as np
import math

def find_candidates(input_frame, size_block, num_candidates):
    image = cv2.imread("original_frames/" + input_frame)
    rows, cols, license = np.shape(image)
    candidates = np.empty([size_block, size_block, license, num_candidates])
    y_max = rows - size_block
    x_max = cols - size_block 

    for i in range(num_candidates):
        x1 = random.randint(0,x_max)
        y1 = random.randint(0,y_max)

        x2 = x1 + size_block
        y2 = y1 + size_block
        current_candidate = image[y1:y2,x1:x2,:]
        candidates[:,:,:,i] = current_candidate
    candidates = candidates.astype(int)
    return candidates 

def Compute_SSD(A,B):
    s = np.sum((A[:,:,0:3]-B[:,:,0:3])**2)
    return s 

def texture_match(input_frame,candidates,overlap_size,size_block):
    image = cv2.imread("original_frames/" + input_frame)
    rows, cols, license = np.shape(image)
    rows_c, cols_c, license_c, num = np.shape(candidates)
    for v in range(74,126,size_block):
        for u in range (59,290,size_block):
            frame_left = image[v:v+size_block,u-size_block:u,:]
            frame_top = image[v-size_block:v,u:u+size_block,:]
            left_overlap_r = frame_left[:,size_block-overlap_size:] 
            top_overlap_r = frame_top[size_block-overlap_size:,:]
            winner = 0; 
            current_ssd = math.inf 
            for i in range(num):
                cand = candidates[:,:,:,i]
                cand_left_overlap = cand[:,0:overlap_size]
                cand_top_overlap = cand[0:overlap_size,:]
                ssd_1 = Compute_SSD(left_overlap_r,cand_left_overlap)
                ssd_2 = Compute_SSD(top_overlap_r, cand_top_overlap)
                ssd = ssd_1 + ssd_2
                if ssd < current_ssd:
                    winner = i;
                    current_ssd = ssd; 
            image[v:v+size_block,u:u+size_block,:] = candidates[:,:,:,i]
    cv2.imwrite("Test.jpg", image) 
            
