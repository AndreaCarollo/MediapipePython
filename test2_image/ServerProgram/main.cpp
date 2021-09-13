#include <zmq.hpp>
#include <iostream>
#include <unistd.h>
#include <opencv2/opencv.hpp>

int main()
{

    //  Prepare our context and socket
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_REP); // ZMQ_PUB);
    socket.bind("tcp://*:5555");

    cv::Mat test_img = cv::imread("../test.png"); // , cv::IMREAD_GRAYSCALE);
    test_img.convertTo(test_img, CV_8UC3);

    int height = test_img.rows;
    int width = test_img.cols;
    // zmq_send(socket, test_img.data, (height * width * sizeof(uint)), ZMQ_NOBLOCK);

    cv::imshow("img c++", test_img);
    cv::waitKey(0);
    cv::destroyAllWindows();

    // forever loop
    zmq::message_t request, request_2, request_3;
    std::string replyMessage;
    while (true)
    {
        socket.recv(&request);
        replyMessage = std::string(static_cast<char *>(request.data()), request.size());
        std::cout << "Received from client: " + replyMessage << std::endl;

        if (replyMessage == "py req img")
        {
            std::cout << "This: send img" << std::endl;
            zmq_send(socket, test_img.data, (3 * height * width * sizeof(uint8_t)), ZMQ_NOBLOCK);

            //  Wait for next request from client
            socket.recv(&request_2);
            replyMessage = std::string(static_cast<char *>(request_2.data()), request_2.size());
            std::cout << "Received from client: " + replyMessage << std::endl;
            if (replyMessage == "received img")
            {
                std::cout << "Received from client: " + replyMessage << std::endl;

                //  Send reply back to client
                std::string msgToClient("pippo");
                zmq::message_t reply(msgToClient.size());
                memcpy((void *)reply.data(), (msgToClient.c_str()), msgToClient.size());
                socket.send(reply);

                // std::cout << "This: wait for elaboration on py" << std::endl;

                // socket.recv(&request_3);
                // std::string replyMessage = std::string(static_cast<char *>(request_2.data()), request_2.size());
                // // std::string replyMessage = std::string((request.data())., request.size());
                // // // Print out received message
                // std::cout << "Received from client: " + replyMessage << std::endl;
            }
        }

        // //  See the gradual sending/replying from client
        // sleep(1);

        // //  Send reply back to client
        // std::string msgToClient("greeting from C++");
        // zmq::message_t reply(msgToClient.size());
        // memcpy((void *)reply.data(), (msgToClient.c_str()), msgToClient.size());
        // socket.send(reply);
    }
    return 0;
}
