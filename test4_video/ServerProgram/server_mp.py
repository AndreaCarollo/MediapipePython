
from os import wait
import zmq
import numpy
import cv2
import pose_estimation_class as pm
import mediapipe as mp
import detector_pedestrian as dp


context = zmq.Context()
socket = context.socket(zmq.REP)
port = "5555"
socket.bind("tcp://*:5555") # % port)
req_elaboration = "py req elaboration image"
# fix dimension for the moment
width = 1080; # My image width
height = 1920; # My image height

# init detector
detector = pm.PoseDetector(True,False,False,0.5,0.0)
pedestrian = dp.PedestrianDetector()

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
        # Converting bytes data to ndarray
        image = numpy.frombuffer(image_byte,dtype=numpy.uint8).reshape((height,width,3))
        
        # elaboration
        img, p_landmarks, p_connections = detector.findPose(image, False)
        mp.solutions.drawing_utils.draw_landmarks(img, p_landmarks, p_connections)
        lmList = detector.getPosition(img)
        
        pedestrian.executeNet(image)
        # show image
        cv2.imshow("Python image received", image)
        cv2.waitKey(1)



        socket.send_string("elaboration done")
        print("elaboration done")


