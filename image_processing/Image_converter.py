import cv2


image = cv2.imread("/home/barbara/Pictures/pyramid_rock.jpg", 0)

# Image size
width, height = image.shape

# image resize
width = 1920
height = 1080
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

while True:

    cv2.imshow("pyramid_rock.png", image)

    # Quit Esc and timing
    k = cv2.waitKey(100) & 0xFF
    if k == 27:  # esc
        break

    # press "s" to save
    if k == ord("s"):
        cv2.imwrite("../images/new_save.png", image)

cv2.destroyAllWindows()
