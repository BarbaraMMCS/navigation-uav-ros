import cv2
import numpy as np

# Load image
image = cv2.imread("/home/barbara/Pictures/NikonDF_0026.jpg")

# Image size
shape = image.shape
print(shape)

# RGB colors
white_rgb = (255, 255, 255)
blue_rgb = (255, 0, 0)
red_rgb = (0, 0, 255)
green_rgb = (0, 255, 0)
violet_rgb = (170, 0, 170)
yellow_rgb = (0, 170, 170)

# Shapes
cv2.line(image, (3200, 2000), (4200, 2000), green_rgb, 2)
cv2.circle(image, (3700, 1750), 10, red_rgb, -1)
cv2.ellipse(image, (3700, 2000), (500, 300), 180, 180, 0, green_rgb, 3)
points = np.array([[[2000, 1000], [2000, 1250], [1300, 1200], [2300, 1400]]], np.int32)
cv2.polylines(image, [points], True, yellow_rgb, thickness=2)
cv2.circle(image, (1500, 2400), 10, blue_rgb, -1)

# Text
font = cv2.FONT_HERSHEY_TRIPLEX
cv2.putText(image, "pyramid rock", (3200, 1600), font, 4, violet_rgb)

# Region of interest
# row, column, chanel = shape
pt1 = (1200, 2200)
pt2 = (1800, 2600)
pt1_x, pt1_y = pt1
pt2_x, pt2_y = pt2
cv2.rectangle(image, pt1, pt2, white_rgb, 3)
roi = image[pt1_y:pt2_y, pt1_x:pt2_x] # ratio is 2:3 --> [1:row, 1.5:column]

# image resize after so shapes keeps position
width = 720
height = 480
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
roi = cv2.resize(roi, dim, interpolation=cv2.INTER_AREA)

row, column, chanel = image.shape

scaled_image = cv2.resize(roi, None, fx=1/2, fy=1/2)

cv2.imwrite("image.png", image)
image = cv2.imread("/home/barbara/Pictures/image.jpg")

matrix = np.float32([[1, 0, 50], [1, 0, 50]])
translation_img = cv2.warpAffine(roi, matrix, (column, row))

print("Height: ", row)
print("Width: ", column)


# window
cv2.imshow("pyramid_rock", image)
cv2.imshow("ROI", scaled_image)
cv2.imshow("translation_img", translation_img)


# quit
cv2.waitKey(0) & 0xFF == ord("q")
cv2.destroyAllWindows()
