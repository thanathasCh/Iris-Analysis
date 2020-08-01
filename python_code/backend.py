import cv2
import numpy as np
import imutils

def start(img, limitWidth, currentX, currentY, currentHeight, currentWidth):
    h, w, _ = img.shape
    new_size = (int((limitWidth / w) * h), limitWidth)
    new_img = imutils.resize(img, width=limitWidth, height=int((limitWidth / w) * h))


    cv2.rectangle(new_img, (currentX, currentY), (currentX + currentWidth, currentY + currentHeight), (255, 0, 0), 10)
    cv2.imshow('a', new_img)
    cv2.waitKey()