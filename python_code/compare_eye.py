import cv2
import numpy as np
from skimage.measure import compare_ssim
import imutils
import os

def blur(img):
    # kernel = np.ones((5,5),np.float32)/25
    # dst = cv2.filter2D(img,-1,kernel)
    dst = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
    return dst

def compare(img1, img2, i):
    (score, diff) = compare_ssim(img1, img2, full=True)
    diff = (diff * 255).astype("uint8")
    
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cv2.imwrite("result/diff.png", diff)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w < 50 and h < 50:
            cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 1)

    cv2.imwrite("result/diff_detected" + str(i) + ".png", diff)
    # cv2.imwrite("thresh.png", thresh)
    # cv2.imwrite("img1_result.png", img1)
    cv2.imwrite("result/right_detected" + str(i) + ".png", img2)

def start():
    PATH = "clean_datasets/right/"
    counter = 1
    for i in os.listdir(PATH):
        clean = cv2.imread(PATH+i)
        # clean = cv2.imread("clean_datasets/left/clean_left" + str(i+1) + ".png")
        diseased = cv2.imread("result/eye.png")

        clean_blur = blur(clean)
        diseased_blur = blur(diseased)

        clean_resize = cv2.resize(clean_blur, (300, 300), interpolation = cv2.INTER_AREA)
        diseased_resize = cv2.resize(diseased_blur, (300, 300), interpolation = cv2.INTER_AREA)

        clean_gray = cv2.cvtColor(clean_resize, cv2.COLOR_BGR2GRAY)
        diseased_gray = cv2.cvtColor(diseased_resize, cv2.COLOR_BGR2GRAY)

        compare(clean_gray, diseased_gray, counter)
        counter += 1