import video
import tracking
import os

video.decomposeVideo("Original.avi", "original_frames", 400)

for file in os.listdir("original_frames"):
    tracking.find_pen(file)

video.composeVideo("original_frames", "result.avi", 15)