import cv2
import numpy as np

capture = cv2.VideoCapture(0)
# if video from a file : change 0 by name.extension, if multiple camera change to 1
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# codec to save
output = cv2.VideoWriter("output.avi", fourcc, 15.0, (640, 480))
# create instances output (name to save, codec, fps, size)


while (capture.isOpened()):
    # captures the frame
    ret, frame = capture.read()

    if ret == True:

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Because hsv is easier to deal with

        output.write(frame)
        # saves the file

        # color filters
        # Gray filter
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        # Blue
        low_blue = np.array([94, 80, 2])
        high_blue = np.array([126, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
        blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

        # Red
        low_red = np.array([161, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        red = cv2.bitwise_and(frame, frame, mask=red_mask)

        # Green
        low_green = np.array([25, 52, 72])
        high_green = np.array([102, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)

        # Every color except white
        low = np.array([0, 42, 0])
        high = np.array([179, 255, 255])
        mask = cv2.inRange(hsv_frame, low, high)
        not_white = cv2.bitwise_and(frame, frame, mask=mask)

        # Blur filter
        kernel = np.ones((15, 15), np.float32)/225

        smoothed = cv2.filter2D(frame, -1, kernel)
        blur = cv2.GaussianBlur(frame, (15, 15), 0)
        median = cv2.medianBlur(frame, 15)
        bilateral = cv2.bilateralFilter(frame, 15, 75, 75)

        # Show windows
        cv2.imshow("Color", frame)
        cv2.imshow("Gray", gray)
        cv2.imshow("Red", red)
        cv2.imshow("Blue", blue)
        cv2.imshow("Green", green)
        cv2.imshow("Not white", not_white)
        cv2.imshow("Smoothed", smoothed)
        cv2.imshow("Blur", blur)
        cv2.imshow("Median", median)
        cv2.imshow("Bilateral", bilateral)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            # quit key
            break
    else:
        break

capture.release()
output.release()
cv2.destroyAllWindows()
