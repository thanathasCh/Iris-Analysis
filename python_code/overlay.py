import cv2

def start():
    background = cv2.imread('result/coor.png')
    overlay = cv2.imread('static/images/eye-pattern.png')
    overlay = cv2.resize(overlay, background.shape[:2])
    added_image = cv2.addWeighted(background,1,overlay,0.2,0)

    cv2.imshow('combined', added_image)
    cv2.imwrite('result/coor_overlay.png', added_image)
    cv2.waitKey()