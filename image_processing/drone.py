import cv2
import numpy as np
import time


def nothing(x):
    pass


# Load file
capture = cv2.VideoCapture("/home/barbara/Videos/Drone/DJI_0004.MOV")

# Live webcam, 0 = first webcam, 1 = next one
#capture = cv2.VideoCapture(0)


# Set FPS for files and drone feed
frame_rate = 30
# WEBCAM fps = frame_rate times 1000 -----> Because every loop = 1 ms. Use in WaitKey(fps)
fps = frame_rate * 1000

# Frame counter
total_frames = 0
# Time counter
prev = 0

# Video codec and parameters for save (overwrite) --> XVID saves file.avi
# To know original size uncomment : print(final_frame.shape) inside the while loop
codec = cv2.VideoWriter_fourcc(*'MJPG')
recorder = cv2.VideoWriter("last_recorded.avi", codec, 15.0, (3840, 2160))

# Create sliders
cv2.namedWindow("Drone_sliders")

# Fps parameter slider
cv2.createTrackbar("FPS", "Drone_sliders", frame_rate, 60, nothing)

# Mask color HSV
cv2.createTrackbar("Lower - Hue", "Drone_sliders", 0, 255, nothing)
cv2.createTrackbar("Upper - Hue", "Drone_sliders", 255, 255, nothing)

cv2.createTrackbar("Lower - Saturation", "Drone_sliders", 0, 255, nothing)
cv2.createTrackbar("Upper - Saturation", "Drone_sliders", 255, 255, nothing)

cv2.createTrackbar("Lower - Value", "Drone_sliders", 0, 255, nothing)
cv2.createTrackbar("Upper - Value", "Drone_sliders", 255, 255, nothing)

# Mask switch color HSV
cv2.createTrackbar("Blue", "Drone_sliders", 0, 1, nothing)
cv2.createTrackbar("Red", "Drone_sliders", 0, 1, nothing)
cv2.createTrackbar("Green", "Drone_sliders", 0, 1, nothing)
cv2.createTrackbar("Not_white", "Drone_sliders", 0, 1, nothing)

# Gray filter
cv2.createTrackbar("Gray", "Drone_sliders", 0, 1, nothing)

# Filter blur
cv2.createTrackbar("Smoothed", "Drone_sliders", 0, 1, nothing)
cv2.createTrackbar("Gaussian blur", "Drone_sliders", 0, 1, nothing)
cv2.createTrackbar("Median", "Drone_sliders", 0, 1, nothing)
cv2.createTrackbar("Bilateral", "Drone_sliders", 0, 1, nothing)

# While video run
while capture.isOpened():

    # Time
    time_elapsed = time.time() - prev

    # Extract frame by frame
    ret, i_frame = capture.read()

    # Flip frame : 0 = up side down , 1 = mirror
    i_frame = cv2.flip(i_frame, 1)

    # FPS
    if time_elapsed > 1. / frame_rate:
        prev = time.time()

        # If image feed for live
        if ret:

            # Resize frame
            width = 1080
            height = 720
            dim = (width, height)
            frame = cv2.resize(i_frame, dim, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

            # record 1 frame
            recorder.write(frame)
            total_frames += 1

            # Fps print on window
            fps = cv2.getTrackbarPos("FPS", "Drone_sliders")
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(fps), (50, 100), font, 3, (255, 240, 200), 1)

            # convert Red Green Blue to Hue Saturation Value color space
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # filter sliders
            l_h = cv2.getTrackbarPos("Lower - Hue", "Drone_sliders")
            l_s = cv2.getTrackbarPos("Lower - Saturation", "Drone_sliders")
            l_v = cv2.getTrackbarPos("Lower - Value", "Drone_sliders")
            u_h = cv2.getTrackbarPos("Upper - Hue", "Drone_sliders")
            u_s = cv2.getTrackbarPos("Upper - Saturation", "Drone_sliders")
            u_v = cv2.getTrackbarPos("Upper - Value", "Drone_sliders")

            # Mask
            lower = np.array([l_h, l_s, l_v])
            upper = np.array([u_h, u_s, u_v])
            mask = cv2.inRange(hsv_frame, lower, upper)
            final_frame = cv2.bitwise_and(frame, frame, mask=mask)

            # Switch Gray
            switch_gray = cv2.getTrackbarPos("Gray", "Drone_sliders")
            if switch_gray == 0:
                pass
            else:
                final_frame = cv2.cvtColor(final_frame, cv2.COLOR_BGR2GRAY)

            # Switch Blue
            switch_blue = cv2.getTrackbarPos("Blue", "Drone_sliders")
            if switch_blue == 0:
                pass
            else:
                low_blue = np.array([38, 86, 0])
                high_blue = np.array([121, 255, 255])
                blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
                final_frame = cv2.bitwise_and(frame, frame, mask=blue_mask)

            # Switch Red
            switch_red = cv2.getTrackbarPos("Red", "Drone_sliders")
            if switch_red == 0:
                pass
            else:
                low_red = np.array([161, 155, 84])
                high_red = np.array([179, 255, 255])
                red_mask = cv2.inRange(hsv_frame, low_red, high_red)
                final_frame = cv2.bitwise_and(frame, frame, mask=red_mask)

            # Switch Green
            switch_green = cv2.getTrackbarPos("Green", "Drone_sliders")
            if switch_green == 0:
                pass
            else:
                low_green = np.array([-10, 100, 100])
                high_green = np.array([60, 255, 255])
                green_mask = cv2.inRange(hsv_frame, low_green, high_green)
                final_frame = cv2.bitwise_and(frame, frame, mask=green_mask)

            # Switch Not_white
            switch_not_white = cv2.getTrackbarPos("Not_white", "Drone_sliders")
            if switch_not_white == 0:
                pass
            else:
                low = np.array([0, 42, 0])
                high = np.array([179, 255, 255])
                mask = cv2.inRange(hsv_frame, low, high)
                final_frame = cv2.bitwise_and(frame, frame, mask=mask)

            # Switch Smooth blur
            kernel = np.ones((15, 15), np.float32) / 225
            switch_smoothed = cv2.getTrackbarPos("Smoothed", "Drone_sliders")
            if switch_smoothed == 0:
                pass
            else:
                final_frame = cv2.filter2D(frame, -1, kernel)

            # Switch Gaussian Blur
            switch_blur = cv2.getTrackbarPos("Gaussian blur", "Drone_sliders")
            if switch_blur == 0:
                pass
            else:
                final_frame = cv2.GaussianBlur(final_frame, (5, 5), 0)

            # Switch median blur
            switch_median = cv2.getTrackbarPos("Median", "Drone_sliders")
            if switch_median == 0:
                pass
            else:
                final_frame = cv2.medianBlur(final_frame, 15)

            # Switch bilateral blur
            switch_bilateral = cv2.getTrackbarPos("Bilateral", "Drone_sliders")
            if switch_bilateral == 0:
                pass
            else:
                final_frame = cv2.bilateralFilter(final_frame, 15, 75, 75)

            # Show windows
            cv2.imshow("final_frame", final_frame)

            # Data print
            # print(final_frame.shape)
            print("Frame number: ", total_frames, ",  Fps: ", fps, " Time elapse: ", time_elapsed)

            # Quit key q
            if cv2.waitKey(fps) & 0xFF == ord("q"):
                break
        else:
            break

# release and destroy windows
capture.release()
recorder.release()
cv2.destroyAllWindows()
