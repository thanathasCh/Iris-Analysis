import cv2
import numpy as np
import imutils
import json
from tqdm import tqdm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

with open('python_code/polygon.json', 'r') as f:
    polygons = json.load(f)
    f.close()

BLUE = (255, 0, 0)
BORDER = 2


def start(img, limitWidth, currentX, currentY, currentHeight, currentWidth):
    h, w, _ = img.shape
    new_size = (int((limitWidth / w) * h), limitWidth)
    new_img = imutils.resize(img, width=limitWidth, height=int((limitWidth / w) * h))

    r_w = currentHeight / 200
    r_h = currentWidth / 200

    for polygon in polygons:
        for i in range(len(polygon)):
            curr = polygon[i]
            
            if (i != len(polygon) - 1):
                nxt = polygon[i + 1]
                nxtX = int(nxt['x'] * r_w) + currentX
                nxtY = int(nxt['y'] * r_h)+ currentY
            else:
                nxt = polygon[0]
                nxtX = nxt['x']
                nxtY = nxt['y']
            
            curr['x'] = int(curr['x'] * r_w) + currentX
            curr['y'] = int(curr['y'] * r_h) + currentY

            cv2.line(new_img, (curr['x'], curr['y']), (nxtX, nxtY), BLUE, BORDER)

    # polygon_points = []
    # for coor in polygons[0]:
    #     polygon_points.append((Point(coor['x'], coor['y'])))

    # polygon = Polygon(polygon_points)

    # for x in tqdm(range(500)):
    #     for y in range(500):
    #         point = Point(x, y)
    #         if polygon.contains(point):  
    #             pass
    #             # cv2.circle(new_img, (x, y), 2, BLUE, BORDER)

    cv2.imshow('a', new_img)
    cv2.waitKey()