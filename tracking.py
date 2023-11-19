import cv2
import numpy as np

def draw_rect():
    image = cv2.imread("original_frames\\frame0000.jpg")
    hgt, widt = np.shape(image)