#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

using namespace std;
using namespace cv;

class cam_test{
    public:
        cam_test(){
            VideoCapture cap(CV_CAP_ANY);
                if (!cap.isOpened())
                {
                    cout << "Cannot open video" << endl;
                }

                double dwidht = cap.get(CV_CAP_PROP_FRAME_WIDTH);
                double dheight = cap.get(CV_CAP_PROP_FRAME_HEIGHT);

                cout << "Frame size: " << dwidht << " x " << dheight <<  endl;

                namedWindow("MyVideo", CV_WINDOW_AUTOSIZE);

                while (1)
                {
                    Mat frame;

                    bool bSuccess = cap.read(frame);
                        if (!bSuccess)
                        {
                            cout << "Cannot read camera stream" << endl;
                            break;
                        }
                        imshow("MyVideo", frame);

                        if (waitKey(30) == 27) // esc to exit
                        {
                            break;
                        }
                    }
            }

            ~cam_test(){
                cvDestroyWindow("Camera_Output");
            }
};

int main(int argc, char **argv)
{
    ros::init(argc, argv, "video");
    cam_test cam_object;

    ROS_INFO("video works!");
}