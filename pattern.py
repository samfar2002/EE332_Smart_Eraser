import cv2
import random
import numpy as np
import math

def find_candidates(input_frame, size_block, num_candidates):
    image = cv2.imread("original_frames\\" + input_frame)
    rows, cols, license = np.shape(image)
    candidates = []
    y_max = rows - size_block
    x_max = cols - size_block 

    for i in range(num_candidates):
        x1 = random.randint(50,290-size_block)
        y1 = random.randint(0,60-size_block)

        x2 = x1 + size_block
        y2 = y1 + size_block
        current_candidate = image[y1:y2,x1:x2,:]
        candidates.append(current_candidate)
    
    for index, cand in enumerate(candidates):
        cv2.imwrite("candidates\\" + str(index) + ".jpg", cand)
    return candidates 

def Compute_SSD(A,B):
    SSA = np.sum(A[:,:,0:3]**2)
    SSB = np.sum(A[:,:,0:3]**2)
    A_Max = np.max(A)
    B_Max = np.max(B)
    A1 = A/SSA
    B1 = B/SSB
    A2 = A/A_Max
    B2 = B/B_Max
    # S1 normalizes by dividing by the sum of squares in the matrix 
    s1 = np.sum((A1[:,:,0:3]-B1[:,:,0:3])**2)
    # S2 normalizes by dividing by the max in each matrix
    s2 = np.sum((A2[:,:,0:3]-B2[:,:,0:3])**2)
    
    s = s1
    return s

def texture_match(input_frame,candidates,overlap_size,size_block):
    image = cv2.imread("original_frames/" + input_frame)
    rows, cols, license = np.shape(image)
    for v in range(74,126,size_block):
        for u in range (59,290,size_block):
            frame_left = image[v:v+size_block,u-size_block:u,:]
            frame_top = image[v-size_block:v,u:u+size_block,:]
            left_overlap_r = frame_left[:,size_block-overlap_size:] 
            top_overlap_r = frame_top[size_block-overlap_size:,:]
            winner = 0; 
            current_ssd = math.inf 
            for i in range(len(candidates)):
                cand = candidates[i]
                cand_left_overlap = cand[:,0:overlap_size]
                cand_top_overlap = cand[0:overlap_size,:]
                ssd_1 = Compute_SSD(left_overlap_r,cand_left_overlap)
                ssd_2 = Compute_SSD(top_overlap_r, cand_top_overlap)
                ssd = ssd_1 + 5*ssd_2 # Multiply by scaling factor to favor minimizing SSD going up and down
                if ssd < current_ssd:
                    winner = i
                    current_ssd = ssd; 
            image[v:v+size_block,u:u+size_block,:] = candidates[winner] # * 1.1 # Multuply by brightening factor here
    cv2.imwrite("pattern_matched\\" + input_frame, image) 


def write_in_texture(input_frame, pattern_frame, x_coord, lines):
    image = cv2.imread("original_frames\\" + input_frame)
    height, width, color = np.shape(image)
    pattern = cv2.imread(pattern_frame)
    if x_coord < 290:
        section = pattern[60:130, x_coord:290, :]
        image[60:130, x_coord:290, :] = section
    
    num = len([x for x in lines if x>x_coord])
    text = "Covered lines: " + str(num)
    cv2.putText(image, text, (10, height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0,150), 1, cv2.LINE_AA)
    
    cv2.imwrite("new_frames\\" + input_frame, image)
            
