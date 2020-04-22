import cv2
from face_feature_detection import get_control_points

vecA = get_control_points('modi.jpg')
print(vecA)
vecB = get_control_points('shah.jpg')
print(vecB)