import cv2


def get_control_points(img_path):
    def draw_circle(event, x, y, flags, param):
        # draws a circle and saves the point on double click
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
            vec.append((x, y))

    vec = []
    img = cv2.imread(img_path)
    img = cv2.resize(img, (256, 256))
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)

    # exits window on pressing ESC
    while 1:
        cv2.imshow('image', img)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

    return vec
