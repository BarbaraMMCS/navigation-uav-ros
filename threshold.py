import cv2


# useless but needed
def nothing(x):
    pass


# load image in gray
image = cv2.imread("/home/barbara/Pictures/NikonDF_0026.jpg", cv2.IMREAD_GRAYSCALE)
#image = cv2.imread("/home/barbara/Pictures/black_to_white.jpg", cv2.IMREAD_GRAYSCALE)

# image resize
width = 720
height = 480
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# slider
cv2.namedWindow("Image")
cv2.createTrackbar("value", "Image", 128, 255, nothing)

# while image is open
while True:

    # slider value tracker
    value_th = cv2.getTrackbarPos("value", "Image")

    # filters
    _, th_binary = cv2.threshold(image, value_th, 255, cv2.THRESH_BINARY)
    _, th_binary_inv = cv2.threshold(image, value_th, 255, cv2.THRESH_BINARY_INV)
    _, th_trunc = cv2.threshold(image, value_th, 255, cv2.THRESH_TRUNC)
    _, th_to_zero = cv2.threshold(image, value_th, 255, cv2.THRESH_TOZERO)
    _, th_to_zero_inv = cv2.threshold(image, value_th, 255, cv2.THRESH_TOZERO_INV)

    # Show window
    cv2.imshow("th_binary", th_binary)
    cv2.imshow("th_binary_inv", th_binary_inv)
    cv2.imshow("th_to_zero", th_to_zero)
    cv2.imshow("th_to_zero_inv", th_to_zero_inv)
    cv2.imshow("th_trunc", th_trunc)
    cv2.imshow("Image", image)

    # Quit Esc and timing
    k = cv2.waitKey(100) & 0xFF
    if k == 27: #esc
        break

    # press "s" to save
    elif k == ord("s"):
        cv2.imwrite("image_grey.png", image)
        cv2.imwrite("image_th_binary.png", th_binary)
        cv2.imwrite("image_th_binary_inv.png", th_binary_inv)
        cv2.imwrite("image_th_trunc.png", th_trunc)
        cv2.imwrite("image_th_to_zero.png", th_to_zero)
        cv2.imwrite("image_th_to_zero_inv.png", th_to_zero_inv)
        break

cv2.destroyAllWindows()
