#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv)
{
    ros::init(argc, argv, "opencv_pub");
    ros::NodeHandle nodeHandle;
    image_transport::ImageTransport it(nodeHandle);
    image_transport::Publisher pub = it.advertise("image_topic", 1);
    cv::VideoCapture cap;
    bool is_cam_ok = true,
    if(!cap.open(1))
    {
        is_cam_ok = false;
    }
    cv::Mat image;
    ros::Rate loop_rate(10);
    while(nodeHandle.ok())
    {
        if(is_cam_ok)
        {
            cap >> image;

            sensor_msgs::ImagePtr message = cv_bridge::CvImage(std_msgs::Header(), "mono8", image).to ImageMsg();

            pub.publish(message);
            ros::spinOnce();
            loop_rate.sleep();
        }
    }
}