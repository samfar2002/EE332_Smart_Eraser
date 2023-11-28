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

first_coord = tracking.find_pen("frame0000.jpg")
x_coords = tracking.find_pen_ssd(first_coord)

candidates = pattern.find_candidates(frame, size_block, num_candidates)
pattern.texture_match(frame,candidates,overlap_size,size_block)

for index, pic in enumerate(os.listdir("original_frames")):
    print("Writing image", index, "...")
    pattern.write_in_texture(pic, "frame0202.jpg", x_coords[index])

video.composeVideo("new_frames", "new.avi", 15)
