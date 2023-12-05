import video
import tracking
import os
import pattern
import lines

# Break apart video into frames and save into folder
video.decompose_video("Original.avi", "original_frames", 400)

# Set parameters for finding candidates and synthesizing pattern
size_block = 40
num_candidates = 1000
overlap_size = 5
frame = "frame0216.jpg"

# Take a bunch of candidate frames and match the texture to the desired frame
candidates = pattern.find_candidates(frame, size_block, num_candidates)
pattern.texture_match(frame,candidates,overlap_size,size_block)

# Find the spots in between the lines of the synthesized texture
# denoting the gaps between the lines of text
lines.find_dark("finaltexture.jpg")
# Create list of the columns that are where the lines are located
passing_cols = lines.find_lines("test_find.jpg")

# Track the pen to find coordinates of the the pen at each point and
# overlay the bounding rectangle onto the image
first_coord = tracking.find_pen("frame0000.jpg")
x_coords = tracking.find_pen_ssd(first_coord)

# For each picture, fill in the synthesized texture over the red text and
# save into new_frames folder
for index, pic in enumerate(os.listdir("original_frames")):
    print("Writing image", index, "...")
    pattern.write_in_texture(pic, "FinalTexture.jpg", x_coords[index], passing_cols)

# Put the frames back into a video
video.compose_video("new_frames", "new.avi", 15)

