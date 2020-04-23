import cv2


def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)


def is_inside(x1, y1, x2, y2, x3, y3, x, y):
    a = area(x1, y1, x2, y2, x3, y3)
    a1 = area(x, y, x2, y2, x3, y3)
    a2 = area(x1, y1, x, y, x3, y3)
    a3 = area(x1, y1, x2, y2, x, y)
    if a == a1 + a2 + a3:
        return True
    else:
        return False


def get_triangle(triangles, x, y):
    for t in triangles:
        if is_inside(t[0], t[1], t[2], t[3], t[4], t[5], x, y):
            return t
