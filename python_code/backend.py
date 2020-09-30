import cv2
import numpy as np
import imutils
import json
from python_code import compare_eye

with open('python_code/polygon.json', 'r') as f:
    polygons = json.load(f)
    f.close()

BLUE = (255, 0, 0)
BORDER = 2
DRAW = False


def start(img, limitWidth, currentX, currentY, currentHeight, currentWidth, isComplete):
    h, w, _ = img.shape
    new_size = (int((limitWidth / w) * h), limitWidth)
    new_img = cv2.cvtColor(imutils.resize(img, width=limitWidth, height=int((limitWidth / w) * h)), cv2.COLOR_BGR2GRAY)
    new_img[new_img == 0] = 1

    r_w = currentHeight / 200
    r_h = currentWidth / 200

    p1 = (currentX, currentY+currentWidth)
    p2 = (currentX+currentHeight, currentY)
    x = (currentWidth // 2) + currentX
    y = (currentHeight // 2) + currentY
    radiusWidth = currentWidth//2
    radiusHeight = currentHeight//2

    mask = np.zeros_like(new_img)
    mask = cv2.ellipse(mask, (x, y), (radiusWidth, radiusHeight), 0, 0, 360, BLUE, -1)
    result = np.bitwise_and(new_img, mask)
    result[result == 0] = 255

    result = result[p2[1]:p1[1], p1[0]:p2[0]]
    main(result, isComplete)



def main(image, isComplete):
    # You can start working with images over here.
    cv2.imwrite('result/eye.png', image) # samples\30\right\philipr5.bmp

    compare_eye.start()

    cv2.waitKey()