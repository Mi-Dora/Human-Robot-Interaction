from __future__ import division
import time
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2
from object.util import *
import argparse
import os
import os.path as osp
from object.darknet import Darknet
from object.preprocess import prep_image, inp_to_image
import pandas as pd
import random
import pickle as pkl



class Detector(object):
    def __init__(self, save_path="result", batch_size=1, confidence=0.5, nms_thresh=0.4,
                 cfg_file="cfg/yolov3.cfg", weights_file="weight/yolov3.weights", resolution=416, scales="1,2,3"):
        self.save_path = save_path
        self.det = "det"
        self.batch_size = batch_size
        self.confidence = confidence
        self.nms_thresh = nms_thresh
        self.cfgfile = cfg_file
        self.weightsfile = weights_file
        self.reso = resolution
        self.scales = scales

        if not os.path.exists(self.det):
            os.makedirs(self.det)

        self.CUDA = torch.cuda.is_available()

        self.num_classes = 19
        self.classes = load_classes('data/object.names')

        # Set up the neural network
        print("Loading network.....")
        self.model = Darknet(cfg_file)
        self.model.load_weights(weights_file)
        print("Network successfully loaded")

        self.model.net_info["height"] = self.reso
        self.inp_dim = int(self.model.net_info["height"])
        assert self.inp_dim % 32 == 0
        assert self.inp_dim > 32

        # If there's a GPU availible, put the model on GPU
        if self.CUDA:
            self.model.cuda()

        # Set the model in evaluation mode
        self.model.eval()

    def write(self, x, img):
        colors = pkl.load(open("cfg/pallete", "rb"))
        c1 = tuple(x[1:3].int())
        c2 = tuple(x[3:5].int())
        cls = int(x[-1])
        label = "{0}".format(self.classes[cls])
        color = random.choice(colors)
        cv2.rectangle(img, c1, c2, color, 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        cv2.rectangle(img, c1, c2, color, -1)
        cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)
        return img, label

    def crop(self, output, img):
        c1 = tuple(output[1:3].int())
        c2 = tuple(output[3:5].int())
        cls = int(output[-1])
        label = "{0}".format(self.classes[cls])
        cropped = img[c1[1]:c2[1], c1[0]:c2[0]]
        name = osp.join(self.save_path, label+'.jpg')
        cv2.imwrite(name, cropped)

    def detect(self, img):
        """
        :param img:(ndarray) img read by openCV
        :return: bbox
        """

        img_tensor, ori_img, im_dim = prep_image(img, self.reso)
        im_dim = torch.FloatTensor(im_dim).repeat(1, 2)

        if self.CUDA:
            im_dim = im_dim.cuda()

        i = 0

        # load the image
        if self.CUDA:
            img_tensor = img_tensor.cuda()

        # Apply offsets to the result predictions
        # Tranform the predictions as described in the YOLO paper
        # flatten the prediction vector
        # B x (bbox cord x no. of anchors) x grid_w x grid_h --> B x bbox x (all the boxes)
        # Put every proposed box as a row.
        with torch.no_grad():
            prediction = self.model(Variable(img_tensor), self.CUDA)

        # get the boxes with object confidence > threshold
        # Convert the cordinates to absolute coordinates
        # perform NMS on these boxes, and save the results
        # I could have done NMS and saving seperately to have a better abstraction
        # But both these operations require looping, hence
        # clubbing these ops in one loop instead of two.
        # loops are slower than vectorised operations.

        prediction = write_results(prediction, self.confidence,
                                   self.num_classes, nms=True, nms_conf=self.nms_thresh)

        if type(prediction) == int:
            i += 1
            return

        prediction[:, 0] += i * self.batch_size
        output = prediction

        if self.CUDA:
            torch.cuda.synchronize()

        try:
            output
        except NameError:
            print("No detections were made")
            exit()

        im_dim = torch.index_select(im_dim, 0, output[:, 0].long())

        scaling_factor = torch.min(self.reso / im_dim, 1)[0].view(-1, 1)

        output[:, [1, 3]] -= (self.reso - scaling_factor * im_dim[:, 0].view(-1, 1)) / 2
        output[:, [2, 4]] -= (self.reso - scaling_factor * im_dim[:, 1].view(-1, 1)) / 2

        output[:, 1:5] /= scaling_factor

        for i in range(output.shape[0]):
            output[i, [1, 3]] = torch.clamp(output[i, [1, 3]], 0.0, im_dim[i, 0])
            output[i, [2, 4]] = torch.clamp(output[i, [2, 4]], 0.0, im_dim[i, 1])

        list(map(lambda x: self.crop(x, ori_img), output))
        list(map(lambda x: self.write(x, ori_img), output))

        det_names = osp.join(self.det, "10000.jpg")
        cv2.imwrite(det_names, ori_img)


if __name__ == '__main__':

    detector = Detector()
    img = cv2.imread('images/0000_color.jpg')
    detector.detect(img)
    print("Done.")

    torch.cuda.empty_cache()

