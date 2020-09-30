import cv2
import numpy as np
from skimage.measure import compare_ssim
import imutils
import os
from python_code.detect_desease import count_point_in_area
from python_code import overlay

coordinate = []

def isOutSide(img, x, y):
    n_min = np.min(img)
    n_max = np.max(img)

    if img[x, y] == n_max or img[x, y] == n_min:
        return True

    return False

def blur(img):
    # kernel = np.ones((5,5),np.float32)/25
    # dst = cv2.filter2D(img,-1,kernel)
    dst = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
    return dst

def compare(img1, img2, i):
    cv2.waitKey()
    global coordinate
    (score, diff) = compare_ssim(img1, img2, full=True)
    diff = (diff * 255).astype("uint8")
    
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cv2.imwrite("result/diff.png", diff)
    # test = cv2.imread("result/eye.png")

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w < 50 and h < 50:
            if not isOutSide(img2, x, y):
                # cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 255), 1)
                # cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 1)
                """
                color = (0,255,255)
                if i == 1:
                    color = (0,0,255)
                if i == 2:
                    color = (0,255,0)
                if i == 3:
                    color = (255,0,0)
                cv2.rectangle(test, (x, y), (x + 5, y + 5), color, 1)
                """
                coordinate.append((x, y, i))

    # cv2.imwrite("result/test_detected" + str(i) + ".png", test)
    # cv2.imwrite("result/diff_detected" + str(i) + ".png", diff)
    # cv2.imwrite("thresh.png", thresh)
    # cv2.imwrite("img1_result.png", img1)
    # cv2.imwrite("result/eye_detected" + str(i) + ".png", img2)

def start():
    global coordinate

    l_or_r = input("Enter eye (l or r): ")
    if l_or_r == 'l':
        l_or_r = 'left'
    elif l_or_r == 'r':
        l_or_r = 'right'

    PATH = "clean_datasets/" + l_or_r + "/"
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

    coor = cv2.imread("result/eye.png")
    coor = cv2.resize(coor, (300, 300), interpolation = cv2.INTER_AREA)
    for i in coordinate:
        color = (0,255,255)
        if i[2] == 1:
            color = (0,0,255)
        if i[2] == 2:
            color = (0,255,0)
        if i[2] == 3:
            color = (255,0,0)
        cv2.rectangle(coor, (i[0], i[1]), (i[0] + 5, i[1] + 5), color, 1)

    # brain, lung, chest, kidney
    first, second, third, fourth, fifth = count_point_in_area(coor, coordinate)
    sum_coor = first + second + third + fourth + fifth
    # print(first, second, third, fourth, fifth)
    print("There are " + str(sum_coor) + " detected spots in this eye")
    print(str(first) + " (" + str(round((first/sum_coor)*100,2)) + "%)" + " of detected errors are in brain section")
    print(str(second) + " (" + str(round((second/sum_coor)*100,2)) + "%)" + " of detected errors are in lung section")
    print(str(third) + " (" + str(round((third/sum_coor)*100,2)) + "%)" + " of detected errors are in chest section")
    print(str(fourth) + " (" + str(round((fourth/sum_coor)*100,2)) + "%)" + " of detected errors are in kidney section")

    # cv2.imshow("detected_spot", coor)
    cv2.imwrite("result/coor.png", coor)
    overlay.start()
