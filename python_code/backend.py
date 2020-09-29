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
    # polygon_shapes = []
    # polygon_boxes = []

    # for polygon in polygons:
    #     polygon_points = []
    #     point_x = []
    #     point_y = []

    #     for i in range(len(polygon)):
    #         curr = polygon[i]
            
    #         if (i != len(polygon) - 1):
    #             nxt = polygon[i + 1]
    #             nxtX = int(nxt['x'] * r_w) + currentX
    #             nxtY = int(nxt['y'] * r_h)+ currentY
    #         else:
    #             nxt = polygon[0]
    #             nxtX = nxt['x']
    #             nxtY = nxt['y']
            
    #         curr['x'] = int(curr['x'] * r_w) + currentX
    #         curr['y'] = int(curr['y'] * r_h) + currentY

    #         polygon_points.append(Point(curr['x'], curr['y']))
    #         point_x.append(curr['x'])
    #         point_y.append(curr['y'])

    #         if DRAW:
    #             cv2.line(new_img, (curr['x'], curr['y']), (nxtX, nxtY), BLUE, BORDER)

    #     polygon_shapes.append(Polygon(polygon_points))

    #     max_x = max(point_x)
    #     min_x = min(point_x)
    #     max_y = max(point_y)
    #     min_y = min(point_y)

    #     polygon_boxes.append([(min_x, min_y), (max_x, max_y)])


    # for x in tqdm(range(500)):
    #     for y in range(500):
    #         point = Point(x, y)

    #         if not polygon_shapes[0].contains(point):# and not polygon_shapes[1].contains(point) and not polygon_shapes[2].contains(point) and not polygon_shapes[3].contains(point) and not polygon_shapes[4].contains(point):
    #             new_img[y, x] = [0, 0, 0]

    # new_images = []
    # for i in range(len(polygon_boxes)):
    #     (x1, y1), (x2, y2) = polygon_boxes[i]
    #     new_images.append(new_img[y1:y2, x1:x2])

    main(result, isComplete)



def main(image, isComplete):
    # You can start working with images over here.
    cv2.imshow('image', image)
    cv2.waitKey()