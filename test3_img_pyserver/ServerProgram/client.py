import zmq
import numpy
import cv2
import mediapipe

context = zmq.Context()
socket = context.socket(zmq.REP)
port = "5555"
socket.bind("tcp://*:5555") # % port)
req_elaboration = "py req elaboration image"
while True:
    # wait the request
    request = socket.recv_string()
    # if request elaboration image
    if request == req_elaboration:
        # reply to send image
        socket.send_string("send image")
        # data of image
        image_byte = socket.recv()
        print("Received image from C++")
        # fix dimension for the moment
        width = 848; # My image width
        height = 480; # My image height
        # Converting bytes data to ndarray
        image = numpy.frombuffer(image_byte,dtype=numpy.uint8).reshape((height,width,3))
        # show image
        cv2.imshow("Python image received", image)
        cv2.waitKey(1000) # wait 1 second
        cv2.destroyAllWindows()
        socket.send_string("elaboration done")
        print("elaboration done")


