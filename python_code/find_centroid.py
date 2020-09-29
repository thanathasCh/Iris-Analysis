from random import seed
from random import randint
import numpy as np
from matplotlib import pyplot as plt
import cv2
from sklearn.cluster import KMeans

board = np.zeros((300, 300), np.uint8)
board = cv2.cvtColor(board, cv2.COLOR_GRAY2BGR)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
arr = []

for _ in range(20):
    arr.append([randint(10, 290), randint(10, 290)])

arr = np.array(arr)
km = KMeans(n_clusters=5)
km.fit(arr)
data = km.labels_
# print(data)

for p, l in zip(arr, data):
    cv2.putText(board, str(l), (p[0], p[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, BLUE, 1)
    cv2.circle(board, (p[0], p[1]), 2, BLUE, 2)

m_l = max(data)

for i in range(m_l+1):
    g = arr[data==i]
    length = g.shape[0]
    sum_x = np.sum(g[:, 0])
    sum_y = np.sum(g[:, 1])

    cen = (sum_x//length, sum_y//length)
    cv2.circle(board, cen, 2, RED, 2)
    m_h = max(g[:, 0] - cen[0])
    m_w = max(g[:, 1] - cen[1])
    cv2.ellipse(board, cen, (m_h+25, m_w+5), 0, 0, 360, RED, 2)

cv2.imshow('a', board)
cv2.waitKey()