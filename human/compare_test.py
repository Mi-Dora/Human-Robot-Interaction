from face_compare import *
import cv2

if __name__ == '__main__':
    cv2_img = cv2.imread('images/obama3.jpg')
    face_compare(cv2_img)