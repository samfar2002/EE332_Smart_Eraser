import cv2
import random
import numpy as np
import math

# find_candidates:
#
# Finds the input number of candidates from the region to use in
# the texture synthesis
def find_candidates(input_frame, size_block, num_candidates):
    # Reads the image and shape
    image = cv2.imread("original_frames\\" + input_frame)

    # For the number of candidates we are looking to save, Randomly generate
    # an x and y value in the correct range and save the array of the
    # correct size beginning at those coordinates
    candidates = []
    for i in range(num_candidates):
        x1 = random.randint(50,290-size_block)
        y1 = random.randint(0,60-size_block)

        x2 = x1 + size_block
        y2 = y1 + size_block
        current_candidate = image[y1:y2,x1:x2,:]
        candidates.append(current_candidate)
    
    # Return the list of candidate arrays
    return candidates 



# compute_SSD:
#
# Finds the normalized SSD of the matrix based on the overall
# brightness of the array
def compute_SSD(A,B):
    # Computer ssd to begin with
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



# texture_match:
#
# Synthesizes the reference pattern based on the input parameters
def texture_match(input_frame,candidates,overlap_size,size_block):
    # Read the image
    image = cv2.imread("original_frames/" + input_frame)
    rows, cols, license = np.shape(image)
    # For each section in the region that we are overwriting, compare each candidate
    # for the specific overlap and determine the best one
    for v in range(74,126,size_block):
        for u in range (59,290,size_block):
            # Get the overlapping regions
            frame_left = image[v:v+size_block,u-size_block:u,:]
            frame_top = image[v-size_block:v,u:u+size_block,:]
            left_overlap_r = frame_left[:,size_block-overlap_size:] 
            top_overlap_r = frame_top[size_block-overlap_size:,:]
            # Intialize the winner and winning ssd
            winner = 0; 
            current_ssd = math.inf 
            # For each candidate, calculate the ssd and assign the new winner
            for i in range(len(candidates)):
                cand = candidates[i]
                cand_left_overlap = cand[:,0:overlap_size]
                cand_top_overlap = cand[0:overlap_size,:]
                ssd_1 = compute_SSD(left_overlap_r,cand_left_overlap)
                ssd_2 = compute_SSD(top_overlap_r, cand_top_overlap)
                # Multiply by scaling factor to favor minimizing SSD going up and down
                ssd = ssd_1 + 5*ssd_2
                # If the ssd is small enough, save this candidate as the
                # one to be overwritten in the spot
                if ssd < current_ssd:
                    winner = i
                    current_ssd = ssd; 
            # Overwrite that part of the image with the winner
            image[v:v+size_block,u:u+size_block,:] = candidates[winner]

    # Save the resulting image
    cv2.imwrite("pattern_matched\\" + input_frame, image) 



# write_in_texture:
#
# Fills in the texture up to the point specified by the location of the pen
def write_in_texture(input_frame, pattern_frame, x_coord, lines):
    # Read the image
    image = cv2.imread("original_frames\\" + input_frame)
    height, width, color = np.shape(image)
    # Read the reference pattern to fill in
    pattern = cv2.imread(pattern_frame)

    # Within the region we want to overwrite
    if x_coord < 290:
        # Replace the section of the image up to the x coordinate
        # with the reference pattern
        section = pattern[60:130, x_coord:290, :]
        image[60:130, x_coord:290, :] = section
    
    # Write in the corner how many lines have been covered with the synthesized pattern
    num = len([x for x in lines if x>x_coord])
    text = "Covered lines: " + str(num)
    cv2.putText(image, text, (10, height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0,150), 1, cv2.LINE_AA)
    
    # Save the image
    cv2.imwrite("new_frames\\" + input_frame, image)
            
