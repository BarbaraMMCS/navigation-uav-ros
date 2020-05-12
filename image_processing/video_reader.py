import numpy as np
import cv2
import time


cap = cv2.VideoCapture('/home/barbara/Videos/output.avi')
time.sleep(2)

while (cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        print("Sucessfully read one frame.")
    else:
        print("Failed to read one frame.")
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)

    # Quit key q
    if cv2.waitKey(0) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()