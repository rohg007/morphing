import cv2
from face_feature_detection import get_control_points
from triangulation import triangulate

# Reading both images and resizing them to a same size
img_modi = cv2.imread('modi.jpg')
img_modi = cv2.resize(img_modi, (512, 512))
img_shah = cv2.imread('shah.jpg')
img_shah = cv2.resize(img_shah, (512, 512))
print(img_modi[0][0])
print(img_modi[511][0])

vecA = get_control_points('modi.jpg')
print(vecA)
triangulate(img_modi, vecA)
vecB = get_control_points('shah.jpg')
triangulate(img_shah, vecB)