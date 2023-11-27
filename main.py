import video
import tracking
import os
import pattern

video.decomposeVideo("Original.avi", "original_frames", 400)

# Probably collect frames here?
size_block = 20
num_candidates = 100
overlap_size = 5
frame = "frame0216.jpg"

first_coords = tracking.find_pen("frame0000.jpg")
x_coords = tracking.find_pen_ssd(first_coords)

candidates = pattern.find_candidates(frame, size_block, num_candidates)
candidates = candidates + pattern.find_candidates_second_area(frame, size_block, num_candidates)
pattern.texture_match(frame,candidates,overlap_size,size_block)

video.composeVideo("pattern_matched", "new.avi", 15)
