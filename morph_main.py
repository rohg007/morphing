import cv2
import numpy as np
from face_feature_detection import get_control_points
from triangulation import triangulate
from morph_utils import get_triangle

# Reading both images and resizing them to a same size
img_bush = cv2.imread('Bush.jpg')
img_clinton = cv2.imread('Clinton.jpg')

vecA = get_control_points('Bush.jpg')
triangulate(img_bush, vecA)
vecB = get_control_points('Clinton.jpg')
triangulate(img_clinton, vecB)

for i in range(21):
    vec = []
    for j in range(3):
        px = ((20 - i) / 20) * vecA[j][0] + (i / 20) * vecB[j][0]
        py = ((20 - i) / 20) * vecA[j][1] + (i / 20) * vecB[j][1]
        vec.append((px, py))
    triangulate(np.zeros((512, 512)), vec)


