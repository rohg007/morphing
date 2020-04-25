import cv2


# applies delaunay triangulation to an image using the control points
def triangulate(img, vec):
    size = img.shape
    rect = (0, 0, size[1], size[0])
    sd = cv2.Subdiv2D(rect)
    for p in vec:
        sd.insert(p)

    # acknowledging border points
    sd.insert((0, 0))
    sd.insert((size[1] - 1, 0))
    sd.insert((0, size[0] - 1))
    sd.insert((size[1] - 1, size[0] - 1))
    triangles = sd.getTriangleList()
    triangleList = []
    for t in triangles:
        p1 = (t[0], t[1])
        p2 = (t[2], t[3])
        p3 = (t[4], t[5])
        cv2.line(img, p1, p2, (255, 255, 0), cv2.LINE_4, 2)
        cv2.line(img, p2, p3, (255, 255, 0), cv2.LINE_4, 2)
        cv2.line(img, p1, p3, (255, 255, 0), cv2.LINE_4, 2)
        temp = [p1, p2, p3]

        # sorting each list of points for effective mapping in subsequent steps
        temp.sort()
        triangleList.append(temp)

    return triangleList
