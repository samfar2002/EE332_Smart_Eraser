import video
import tracking
import os
import pattern

video.decomposeVideo("Original.avi", "original_frames", 400)

# Probably collect frames here?
size_block = 20
num_candidates = 100
frame_0 = "frame0000.jpg"
candidates = pattern.find_candidates(frame_0, size_block, num_candidates, )


for file in os.listdir("original_frames"):
    x_cord = tracking.find_pen(file)
    y_values = tracking.find_textures_to_replace(file,x_cord)

video.composeVideo("original_frames", "result.avi", 15)
