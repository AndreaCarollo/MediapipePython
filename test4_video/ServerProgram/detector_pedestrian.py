#!/usr/bin/env python

from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import time
import logging as log
import numpy as np

from openvino.inference_engine import IECore

from dataclasses import dataclass



class PedestrianDetector:

    def __init__(self):
        self.rectangle_from_detection = []
        self.prob_threshold = 0.85
        self.ie = IECore()
        self.net = self.ie.read_network("/home/user/openvino_models/ir/intel/person-detection-retail-0013/FP16/person-detection-retail-0013.xml",
                                        "/home/user/openvino_models/ir/intel/person-detection-retail-0013/FP16/person-detection-retail-0013.bin")
        self.supported_layers = self.ie.query_network(self.net, "CPU")
        self.img_info_input_blob = None
        self.feed_dict = {}
        for blob_name in self.net.inputs:
            if len(self.net.inputs[blob_name].shape) == 4:
                self.input_blob = blob_name
            elif len(self.net.inputs[blob_name].shape) == 2:
                self.img_info_input_blob = blob_name
            else:
                raise RuntimeError("Unsupported {}D input layer '{}'. Only 2D and 4D input layers are supported"
                                   .format(len(self.net.inputs[blob_name].shape), blob_name))
        self.labels_map = None
        self.out_blob = next(iter(self.net.outputs))
        self.exec_net = self.ie.load_network(network=self.net, num_requests=2, device_name='CPU')
        self.n, self.c, self.h, self.w = self.net.inputs[self.input_blob].shape
        if self.img_info_input_blob:
            self.feed_dict[self.img_info_input_blob] = [self.h, self.w, 1]
    
    def executeNet(self, frame):
        frame_h, frame_w = frame.shape[:2]
        in_frame = cv2.resize(frame, (self.w, self.h))
        in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        in_frame = in_frame.reshape((self.n, self.c, self.h, self.w))
        self.feed_dict[self.input_blob] = in_frame
        # res = self.exec_net.infer(inputs=self.feed_dict)
        # res = self.exec_net.infer(items = in_frame)
        self.exec_net.start_async(request_id=0, inputs=self.feed_dict)
        request_status = self.exec_net.requests[0].wait()
        # res = self.exec_net.requests[0].outputs['prob']
        res = self.exec_net.requests[0].outputs[self.out_blob]
        self.rectangle_from_detection = []
        for obj in res[0][0]:
                # Draw only objects when probability more than specified threshold
                if obj[2] > self.prob_threshold:
                    xmin = int(obj[3] * frame_w)
                    ymin = int(obj[4] * frame_h)
                    xmax = int(obj[5] * frame_w)
                    ymax = int(obj[6] * frame_h)
                    class_id = int(obj[1])

                    self.rectangle_from_detection.append([xmin, ymin, xmax, ymax])
                    # Draw box and label\class_id
                    color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                    # Draw only objects when probability more than specified threshold
                    det_label = self.labels_map[class_id] if self.labels_map else str(class_id)
                    cv2.putText(frame, det_label + ' ' + str(round(obj[2] * 100, 1)) + ' %', (xmin, ymin - 7),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)
        return self.rectangle_from_detection






