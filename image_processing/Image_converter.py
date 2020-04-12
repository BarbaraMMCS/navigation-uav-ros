import cv2


image = cv2.imread("ROS_diagram.png", cv2.IMREAD_GRAYSCALE)

# Image size
shape = image.shape
print(shape)
width, height = shape

# image resize

factor = 0.20
width_r, height_r = width*factor, height*factor
print(width_r, height_r)
dim = (int(width_r), int(height_r))

image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

while True:

    cv2.imshow("ROS_diagram.png", image)

    # Quit Esc and timing
    k = cv2.waitKey(100) & 0xFF
    if k == 27:  # esc
        break

    # press "s" to save
    if k == ord("s"):
        cv2.imwrite("../images/ROS_diagram_1.png", image)

cv2.destroyAllWindows()
