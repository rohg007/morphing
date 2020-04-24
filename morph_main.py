import cv2
import numpy as np
from face_feature_detection import get_control_points
from triangulation import triangulate
from morph_utils import get_triangle


def display(window, img):
    cv2.imshow(window,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Reading both images and resizing them to a same size
img_src = cv2.imread('Bush.jpg')
img_src2 = cv2.imread('Bush.jpg')
img_src = cv2.resize(img_src, (256, 256))
img_src2 = cv2.resize(img_src, (256, 256))
img_dest = cv2.imread('Clinton.jpg')
img_dest2 = cv2.imread('Clinton.jpg')
img_dest = cv2.resize(img_dest, (256, 256))
img_dest2 = cv2.resize(img_dest, (256, 256))

vecA = get_control_points('Bush.jpg')
print(vecA)
triA = triangulate(img_src2, vecA)
display("Triangulated Bush", img_src2)
cv2.imwrite("triangulated_bush.jpg", img_src2)
triA.sort()
vecB = get_control_points('Clinton.jpg')
triB = triangulate(img_dest2, vecB)
display("Triangulated Bush",  img_dest2)
cv2.imwrite("triangulated_clinton.jpg", img_dest2)
triB.sort()

# ach = 1
outp = []

for i in range(0, 51):
    st = 'inm_bush2clinton'
    ext = '.jpg'
    f_name = st + str(i) + ext
    outp.append(f_name)
    # ach = ach+1

for i in range(1, 51):
    vec = []
    for j in range(3):
        px = ((50 - i) / 50) * vecA[j][0] + (i / 50) * vecB[j][0]
        px = round(px)
        py = ((50 - i) / 50) * vecA[j][1] + (i / 50) * vecB[j][1]
        py = round(py)
        vec.append((px, py))
    tri = triangulate(np.zeros((256, 256), np.uint8), vec)
    tri.sort()
    int_frm = np.zeros((256, 256, 3), np.uint8)
    for k in range(256):
        for l in range(256):
            ind = get_triangle(tri, k, l)
            x0 = tri[ind][0][0]
            y0 = tri[ind][0][1]
            x1 = tri[ind][1][0]
            y1 = tri[ind][1][1]
            x2 = tri[ind][2][0]
            y2 = tri[ind][2][1]

            alpha = (((x2 - x0) * (l - y0) - (k - x0) * (y2 - y0)) / ((x2 - x0) * (y1 - y0) - (x1 - x0) * (y2 - y0)))
            beta = (((x1 - x0) * (l - y0) - (k - x0) * (y1 - y0)) / ((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)))

            xs = triA[ind][0][0] + alpha * (triA[ind][1][0] - triA[ind][0][0]) + beta * (triA[ind][2][0] - triA[ind][0][0])
            ys = triA[ind][0][1] + alpha * (triA[ind][1][1] - triA[ind][0][1]) + beta * (triA[ind][2][1] - triA[ind][0][1])
            xs = int(round(xs))
            ys = int(round(ys))

            xd = triB[ind][0][0] + alpha * (triB[ind][1][0] - triB[ind][0][0]) + beta * (triB[ind][2][0] - triB[ind][0][0])
            yd = triB[ind][0][1] + alpha * (triB[ind][1][1] - triB[ind][0][1]) + beta * (triB[ind][2][1] - triB[ind][0][1])
            xd = int(round(xd))
            yd = int(round(yd))

            int_frm[k][l][0] = ((50 - i) / 50) * (img_src[xs][ys][0]) + (i / 50) * (img_dest[xd][yd][0])
            int_frm[k][l][1] = ((50 - i) / 50) * (img_src[xs][ys][1]) + (i / 50) * (img_dest[xd][yd][1])
            int_frm[k][l][2] = ((50 - i) / 50) * (img_src[xs][ys][2]) + (i / 50) * (img_dest[xd][yd][2])

    cv2.imwrite(outp[i], int_frm)
    print(vec)
