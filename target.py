import cv2
import numpy as np

# load image
image = cv2.imread("/home/barbara/Pictures/NikonDF_0026.jpg")

# tells the image size
shape = image.shape
print(shape)

# RGB colors
white_rgb = (255, 255, 255)
blue_rgb = (255, 0, 0)
red_rgb = (0, 0, 255)
green_rgb = (0, 255, 0)
violet_rgb = (170, 0, 170)
yellow_rgb = (0, 170, 170)

# shapes onto original size
cv2.line(image, (3200, 2000), (4200, 2000), green_rgb, 2)
cv2.circle(image, (3700, 1750), 10, red_rgb, -1)
cv2.ellipse(image, (3700, 2000), (500, 300), 180, 180, 0, green_rgb, 3)
cv2.rectangle(image, (1200, 2200), (1800, 2600), white_rgb, 3)
cv2.circle(image, (1500, 2400), 10, blue_rgb, -1)

points = np.array([[[2000, 1000], [2000, 1250], [1300, 1200], [2300, 1400]]], np.int32)
cv2.polylines(image, [points], True, yellow_rgb, thickness=2)

font = cv2.FONT_HERSHEY_TRIPLEX
cv2.putText(image, "pyramid rock", (3200, 1600), font, 4, violet_rgb)

# image resize after so shapes keeps position
width = 720
height = 480
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# window
cv2.imshow("pyramid_rock", image)

# quit
cv2.waitKey(0)
cv2.destroyAllWindows()
