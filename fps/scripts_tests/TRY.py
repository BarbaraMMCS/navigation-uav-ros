


def nothing(x):
    pass


# Set FPS for files and drone feed
frame_rate = 15
# WEBCAM fps = frame_rate times 1000 -----> Because every loop = 1 ms. Use in WaitKey(fps)
fps = frame_rate * 1000
# Frame counter
total_frames = 0
# Time counter
prev = 0
# Video codec and parameters for save (overwrite) --> XVID saves last_recorded.avi
codec = cv2.VideoWriter_fourcc(*"XVID")
recorder = cv2.VideoWriter("last_recorded.avi", codec, 15.0, (3840, 2160))


# Create sliders
cv2.namedWindow("Drone_sliders")

# Fps parameter slider
cv2.createTrackbar("FPS", "Drone_sliders", frame_rate, 60, nothing)
# Gray filter switch
cv2.createTrackbar("Gray", "Drone_sliders", 0, 1, nothing)



def callback(data):
    i_frame = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

    # Time and fps
    time_elapsed = time.time() - prev
    if time_elapsed > 1 / frame_rate:
        prev = time.time()

        if (i_frame.any()):        
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

            # Switch Gray
            switch_gray = cv2.getTrackbarPos("Gray", "Drone_sliders")
            if switch_gray == 0:
                pass
            else:
                final_frame = cv2.cvtColor(final_frame, cv2.COLOR_BGR2GRAY)

            # Data print
            print("Frame number: ", (total_frames))
            print("Fps: ", (fps))
            print("Frame number: ", (time_elapsed))

            # Show windows
            cv2.imshow("video", final_frame)


            if cv2.waitKey(fps) & 0xFF == ord('q'):
                recorder.release()
                cv2.destroyAllWindows()

            cv2.destroyAllWindows()


while not rospy.is_shutdown():
    rospy.spin()





