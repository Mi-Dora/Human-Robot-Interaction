#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from face_compare_baidu import *
import cv2
import time

if __name__ == '__main__':
    Aim_img = cv2.imread('images/obama3.jpg')
    New_img = cv2.imread('images/obama2.jpg')
    start = time.time()
    i = 0
    while i < 3:
        start = time.time()
        score = Get_face_compare_result(Aim_img, New_img)
        print(score)
        if i == 0:
            New_img = cv2.imread('images/obama.jpg')
        if i == 1:
            New_img = cv2.imread('images/biden.jpg')
        i = i + 1
    end = time.time()
    print('Cost time:', end - start)