import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2

with open('python_code/back-up.json') as f:
    polygons = json.load(f)
    f.close()

def count_point_in_area(img, points):
    polygon_shapes = []
    polygon_boxes = []
    h, w, _ = img.shape
    r_w = w / 200
    r_h = h / 200
    first = 0
    second = 0
    third = 0
    fourth = 0

    for polygon in polygons:
        polygon_points = []
        point_x = []
        point_y = []

        for i in range(len(polygon)):
            cur = polygon[i]

            if i != len(polygon) - 1:
                nxt = polygon[i + 1]
                nxtX = int(nxt['x'] * r_w)
                nxtY = int(nxt['y'] * r_h)
            else:
                nxt = polygon[0]
                nxtX = nxt['x']
                nxtY = nxt['y']
            
            cur['x'] = int(cur['x'] * r_w)
            cur['y'] = int(cur['y'] * r_h)
            polygon_points.append(Point(cur['x'], cur['y']))
            point_x.append(cur['x'])
            point_y.append(cur['y'])

            # cv2.line(img, (cur['x'], cur['y']), (nxtX, nxtY), (255, 0, 0), 2)

        polygon_shapes.append(Polygon(polygon_points))
        max_x = max(point_x)
        min_x = min(point_x)
        max_y = max(point_y)
        min_y = min(point_y)

        polygon_boxes.append([(min_x, min_y), (max_x, max_y)])

    for x, y, _ in points:
        point = Point(x, y)

        if polygon_shapes[0].contains(point):
            first += 1

        if polygon_shapes[1].contains(point):
            second += 1

        if polygon_shapes[2].contains(point):
            third += 1

        if polygon_shapes[3].contains(point):
            fourth += 1

    return (first, second, third, fourth, len(points) - sum([first, second, third, fourth]))