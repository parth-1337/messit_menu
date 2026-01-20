import cv2
import numpy as np
import glob
import os


for path in glob.glob("images/*.jpg"):
    img = cv2.imread(path)
    if img is None:
        continue

    # Only grayscalling -sharpening kernel removed
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(path, gray)

print("Saved")
