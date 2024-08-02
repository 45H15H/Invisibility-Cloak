import cv2
import numpy as np

# Define the RGB color
# black_rgb = np.uint8([[[23, 19, 21]]]) # For black
black_rgb = np.uint8([[[3, 4, 3]]]) # For black


# Convert RGB to HSV
black_hsv = cv2.cvtColor(black_rgb, cv2.COLOR_RGB2HSV)
print(black_hsv)