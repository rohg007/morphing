import cv2
import numpy as np
from face_feature_detection import get_control_points
from triangulation import triangulate
from morph_utils import get_triangle


# function to display images
def display(window, img):
    cv2.imshow(window, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


src_path = 'Clinton.jpg'
dest_path = 'Bush.jpg'
# Reading both images and resizing them to a same size
img_src = cv2.imread(src_path)
img_src2 = cv2.imread(src_path)
img_src = cv2.resize(img_src, (256, 256))
img_src2 = cv2.resize(img_src, (256, 256))
img_dest = cv2.imread(dest_path)
img_dest2 = cv2.imread(dest_path)
img_dest = cv2.resize(img_dest, (256, 256))
img_dest2 = cv2.resize(img_dest, (256, 256))

# getting control points for each image through mouse clicks
vecA = get_control_points(src_path)
print(vecA)

# triangulating image and getting the list of triangle's vertices
triA = triangulate(img_src2, vecA)
display("Triangulated Clinton", img_src2)
cv2.imwrite("triangulated_clinton.jpg", img_src2)

# sorting triangle list to map triangles correctly in further steps
triA.sort()

vecB = get_control_points(dest_path)
triB = triangulate(img_dest2, vecB)
display("Triangulated Bush", img_dest2)
cv2.imwrite("triangulated_bush.jpg", img_dest2)
triB.sort()

# list to store file names of intermediate frames
outp = []

# number of steps
num_iterations = 80

# generates file name for intermediate frame - inm_bush2clinton(step#).jpg
for i in range(0, num_iterations + 1):
    st = 'inm_bush2clinton'
    ext = '.jpg'
    f_name = st + str(i) + ext
    outp.append(f_name)

for i in range(1, num_iterations + 1):
    # stores control point coordinates for each iteration
    vec = []
    # calculating control point locations for each iteration through weighted average
    for j in range(3):
        px = ((num_iterations - i) / num_iterations) * vecA[j][0] + (i / num_iterations) * vecB[j][0]
        px = round(px)
        py = ((num_iterations - i) / num_iterations) * vecA[j][1] + (i / num_iterations) * vecB[j][1]
        py = round(py)
        vec.append((px, py))

    # triangulating intermediate frames using new control points
    tri = triangulate(np.zeros((256, 256), np.uint8), vec)
    tri.sort()
    int_frm = np.zeros((256, 256, 3), np.uint8)

    for k in range(256):
        for l in range(256):
            # mapping non control point to a triangle in source
            ind = get_triangle(tri, k, l)
            x0 = tri[ind][0][0]
            y0 = tri[ind][0][1]
            x1 = tri[ind][1][0]
            y1 = tri[ind][1][1]
            x2 = tri[ind][2][0]
            y2 = tri[ind][2][1]

            # calculating affine coordinates alpha and beta
            alpha = (((x2 - x0) * (l - y0) - (k - x0) * (y2 - y0)) / ((x2 - x0) * (y1 - y0) - (x1 - x0) * (y2 - y0)))
            beta = (((x1 - x0) * (l - y0) - (k - x0) * (y1 - y0)) / ((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)))

            # mapping affine coordinates & current pixel to a point in source image
            xs = triA[ind][0][0] + alpha * (triA[ind][1][0] - triA[ind][0][0]) + beta * (
                        triA[ind][2][0] - triA[ind][0][0])
            ys = triA[ind][0][1] + alpha * (triA[ind][1][1] - triA[ind][0][1]) + beta * (
                        triA[ind][2][1] - triA[ind][0][1])
            xs = int(round(xs))
            ys = int(round(ys))

            # mapping affine coordinates & current pixel to a point in target
            xd = triB[ind][0][0] + alpha * (triB[ind][1][0] - triB[ind][0][0]) + beta * (
                        triB[ind][2][0] - triB[ind][0][0])
            yd = triB[ind][0][1] + alpha * (triB[ind][1][1] - triB[ind][0][1]) + beta * (
                        triB[ind][2][1] - triB[ind][0][1])
            xd = int(round(xd))
            yd = int(round(yd))

            # setting intensity values through weighted average in three channels
            int_frm[k][l][0] = ((num_iterations - i) / num_iterations) * (img_src[xs][ys][0]) + (i / num_iterations) * (
            img_dest[xd][yd][0])
            int_frm[k][l][1] = ((num_iterations - i) / num_iterations) * (img_src[xs][ys][1]) + (i / num_iterations) * (
            img_dest[xd][yd][1])
            int_frm[k][l][2] = ((num_iterations - i) / num_iterations) * (img_src[xs][ys][2]) + (i / num_iterations) * (
            img_dest[xd][yd][2])

    # saving the intermediate frame
    cv2.imwrite(outp[i], int_frm)
    print(i)

out = cv2.VideoWriter('temp.avi', cv2.VideoWriter_fourcc(*'DIVX'), 40, (256, 256))
out.write(img_src)
for i in range(num_iterations):
    s = 'inm_bush2clinton' + str(i + 1) + '.jpg'
    img = cv2.imread(s)
    out.write(img)
out.write(img_dest)
out.release()