import video
import tracking
import os
import pattern

video.decomposeVideo("Original.avi", "original_frames", 400)

# Probably collect frames here?
size_block = 20
num_candidates = 500
overlap_size = 3
frame_0 = "frame0000.jpg"
candidates = pattern.find_candidates(frame_0, size_block, num_candidates)

first_coords = tracking.find_pen("frame0000.jpg")
x_coords = tracking.find_pen_ssd(first_coords)

pattern.texture_match("frame0000.jpg",candidates,overlap_size,size_block)

video.composeVideo("original_frames", "result.avi", 15)
