import cv2
import os

output_dir = '/home/alan'
i = 1
cap = cv2.VideoCapture('http://192.168.0.3:4747/video')

while 1:
    ret, frame = cap.read()
    cv2.imshow('cap', frame)
    flag = cv2.waitKey(1)
    if flag == 13: #按下回车键
        output_path = os.path.join(output_dir, "%04d.jpg" % i)
        cv2.imwrite(output_path, frame)
        i += 1
    if flag == 27:  #按下ESC键
        break