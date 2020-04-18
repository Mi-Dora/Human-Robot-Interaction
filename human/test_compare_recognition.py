from face_compare_face_rec import *
import cv2
import time

if __name__ == '__main__':
    cv2_img = cv2.imread('images/obama3.jpg')

    start = time.time()
    face_compare(cv2_img)
    end = time.time()
    print('Cost time:', end-start)
