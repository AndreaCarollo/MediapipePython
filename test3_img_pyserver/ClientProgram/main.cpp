#include <zmq.hpp>
#include <iostream>
#include <unistd.h>
#include <opencv2/opencv.hpp>

std::string req_elaboration = "py req elaboration image";
std::string server_send_img = "send image";
std::string server_elaboration_done = "elaboration done";

int main()
{

    //  Prepare our context and socket
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_REQ);
    socket.connect("tcp://localhost:5555");

    cv::Mat test_img = cv::imread("../test.png"); // , cv::IMREAD_GRAYSCALE);
    test_img.convertTo(test_img, CV_8UC3);

    int height = test_img.rows;
    int width = test_img.cols;
    // zmq_send(socket, test_img.data, (height * width * sizeof(uint)), ZMQ_NOBLOCK);

    cv::imshow("img c++", test_img);
    cv::waitKey(10);
    cv::destroyAllWindows();

    zmq::message_t request, request_2, request_3;
    std::string replyMessage;
    
    //  Send requesty to elaborate to server
    std::string msgToServer(req_elaboration);
    zmq::message_t reply(msgToServer.size());
    memcpy((void *)reply.data(), (msgToServer.c_str()), msgToServer.size());
    socket.send(reply);

    socket.recv(&request);
    replyMessage = std::string(static_cast<char *>(request.data()), request.size());
    std::cout << "Received from client: " + replyMessage << std::endl;

    if (replyMessage == server_send_img)
    {
        std::cout << "This: send img" << std::endl;
        zmq_send(socket, test_img.data, (3 * height * width * sizeof(uint8_t)), ZMQ_NOBLOCK);

        //  Wait for next request from client
        socket.recv(&request_2);
        replyMessage = std::string(static_cast<char *>(request_2.data()), request_2.size());
        std::cout << "Received from client: " + replyMessage << std::endl;
        if (replyMessage == server_elaboration_done)
        {
            std::cout << "Finish" << std::endl;
        }
    }

    return 0;
}
