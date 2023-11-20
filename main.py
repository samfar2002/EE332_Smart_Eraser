import video
import tracking

video.decomposeVideo("Original.avi", "original_frames", 400)

tracking.find_pen()