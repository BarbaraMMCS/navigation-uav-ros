#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>


int main(int argc, char** argv)
{
    ros::init(argc, argv, "opencv_pub");

    ros::NodeHandle nh;

    image_transport::ImageTransport it(nh);

    image_transport::Publisher pub = it.advertise("image_topic", 1);

    cv::VideoCapture cap;

    bool is_cam_ok = true;

    if(!cap.open(1))
    {
	ROS_INFO("fail to open camera");
        is_cam_ok = false;
    }

    cv::Mat image;

    ros::Rate loop_rate(5);


    while(nh.ok())
    {
        if(is_cam_ok)
        {
            cap >> image;

            sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8",image).toImageMsg();


            pub.publish(msg);

            ros::spinOnce();

            loop_rate.sleep();
        }
    }
}
