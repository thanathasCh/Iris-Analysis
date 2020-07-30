import cv2
import numpy as np

def start(img, limitWidth, currentX, currentY, currentHeight, currentWidth):
    cv2.imshow('str', img)
    cv2.waitKey()