#include <zmq.hpp>
#include <iostream>
#include <unistd.h>

int main() {
    //  Prepare our context and socket
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_REP);
    socket.bind("tcp://*:5555");

    // forever loop
    while (true) {
        zmq::message_t request;

        //  Wait for next request from client
        socket.recv(&request);
        std::string replyMessage = std::string(static_cast<char *>(request.data()), request.size());
//        std::string replyMessage = std::string((request.data())., request.size());
        // Print out received message
        std::cout << "Received from client: " + replyMessage << std::endl;

        //  See the gradual sending/replying from client
        sleep(1);

        //  Send reply back to client
        std::string msgToClient("greeting from C++");
        zmq::message_t reply(msgToClient.size());
        memcpy((void *) reply.data(), (msgToClient.c_str()), msgToClient.size());
        socket.send(reply);
    }
    return 0;
}
