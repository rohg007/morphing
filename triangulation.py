import cv2


def triangulate(img, vec):
    size = img.shape
    rect = (0, 0, size[1], size[0])
    sd = cv2.Subdiv2D(rect)
    for p in vec:
        sd.insert(p)
    sd.insert((0, 0))
    sd.insert((255, 0))
    sd.insert((0, 255))
    sd.insert((255, 255))
    triangles = sd.getTriangleList()
    # print(triangles)
    triangleList = []
    for t in triangles:
        p1 = (t[0], t[1])
        p2 = (t[2], t[3])
        p3 = (t[4], t[5])
        cv2.line(img, p1, p2, (255, 255, 0), cv2.LINE_4, 2)
        cv2.line(img, p2, p3, (255, 255, 0), cv2.LINE_4, 2)
        cv2.line(img, p1, p3, (255, 255, 0), cv2.LINE_4, 2)
        temp=[]
        temp.append(p1)
        temp.append(p2)
        temp.append(p3)
        triangleList.append(temp)

    cv2.imshow("Triangulated Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return triangleList
