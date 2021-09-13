import zmq
import numpy
import cv2
import io

context = zmq.Context()
socket = context.socket(zmq.REQ)
port = "5555"
socket.connect("tcp://localhost:%s" % port)
# socket.setsockopt_string(zmq.SUBSCRIBE,"")

req_mess = "py req img"

for i in range (1,10):
    socket.send_string("py req img")
    image_byte = socket.recv()
    print("Received reply from C++")
    width = 960; # My image width
    height = 600; # My image height
    # Converting bytes data to ndarray
    image = numpy.frombuffer(image_byte,dtype=numpy.uint8).reshape((height,width,3))
    # image = numpy.frombuffer(image_byte, dtype=numpy.uint8).reshape((height,width))
    cv2.imshow("Python image received", image)
    cv2.waitKey(0)
    socket.send_string("received img")
    
    answer = socket.recv_string()
    socket.send_string("close")


