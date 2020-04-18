#!/usr/bin/env python

from speech.text2speech import synthesize_text
from speech.speechmain import speak
import linecache
from utils.tcp_client import SocketClient
from utils.multi_receive import multi_receive
import os
import cv2
import face_recognition
import requests
from playsound import playsound
from human.face_detect import *
from human.face_compare_baidu import *

# os.remove('./images/name.jpg')
# f = open('./Record.txt', 'r+')
# f.truncate()

list_of_human = ["David", "Jordan", "Lebron"]

Compared_name = list()

def turtlebot_speak(order_of_human):
    if order_of_human == 0:
        print("Hi, gentleman, what's your name?")
        notice_gentleman = "Hi, gentleman, what's your name?"
        synthesize_text(notice_gentleman, 0)
    else:
        print("Speaking: Nice to meet you {}, "
              "what can I do for you?".format(list_of_human[order_of_human - 1]))
        notice_is_human = "Nice to meet you {}, " \
                          "what can I do for you?".format(list_of_human[order_of_human - 1])
        synthesize_text(notice_is_human, order_of_human)

def Human_detect():
    DETECT_TIME = 0
    cap = cv2.VideoCapture(0)  # open the camera, parameter 0 if using the laptop
    while cap.isOpened():
        OK, frame = cap.read()
        if not OK:
            continue
        cv_image = frame
        result = Get_face_result(cv_image)
        # cv2.waitKey(1000)  # open api qps request limit reached
        if result is not None:
            draw_image, FACE_NUM, gender_list = Local_face(cv_image, True)  # Recognize people
            if FACE_NUM == 1:
                cv2.imshow('test', draw_image)
                cv2.waitKey(10)

                # compare if it is the new people
                file = open("Record.txt", "r")
                content = file.read()
                IS_NEW = 0
                IS_OLD = 0
                if len(content) == 0:  # If the Record.txt is blank, the guy must be new.
                    IS_NEW = 1
                    print("IS_NEW = 1")
                else:  # If the Record.txt is not blank, compare with other guy in Record.txt.
                    NAME_NUM = (len(open("Record.txt", 'rU').readlines()))
                    IS_OLD_1 = 0
                    IS_OLD_2 = 0
                    IS_OLD_3 = 0
                    if NAME_NUM == 1:
                        line_content = linecache.getline("Record.txt", 1)
                        name1 = line_content.split('\t')[0]
                        exist_img1 = cv2.imread('./images/' + name1 + '.jpg')
                        IS_OLD_1 = Get_face_compare_result(exist_img1, cv_image)
                    if NAME_NUM == 2:
                        line_content = linecache.getline("Record.txt", 1)
                        name1 = line_content.split('\t')[0]
                        line_content = linecache.getline("Record.txt", 2)
                        name2 = line_content.split('\t')[0]
                        exist_img1 = cv2.imread('./images/' + name1 + '.jpg')
                        exist_img2 = cv2.imread('./images/' + name2 + '.jpg')
                        IS_OLD_1 = Get_face_compare_result(exist_img1, cv_image)
                        IS_OLD_2 = Get_face_compare_result(exist_img2, cv_image)
                    if NAME_NUM == 3:
                        line_content = linecache.getline("Record.txt", 1)
                        name1 = line_content.split('\t')[0]
                        line_content = linecache.getline("Record.txt", 2)
                        name2 = line_content.split('\t')[0]
                        line_content = linecache.getline("Record.txt", 3)
                        name3 = line_content.split('\t')[0]
                        exist_img1 = cv2.imread('./images/' + name1 + '.jpg')
                        exist_img2 = cv2.imread('./images/' + name2 + '.jpg')
                        exist_img3 = cv2.imread('./images/' + name3 + '.jpg')
                        IS_OLD_1 = Get_face_compare_result(exist_img1, cv_image)
                        IS_OLD_2 = Get_face_compare_result(exist_img2, cv_image)
                        IS_OLD_3 = Get_face_compare_result(exist_img3, cv_image)

                    if IS_OLD_1 == -1 or IS_OLD_2 == -1 or IS_OLD_3 == -1:  # Request API fail !!!
                        continue

                    if IS_OLD_1 == 1 or IS_OLD_2 == 1 or IS_OLD_3 == 1:
                        print('You has been recorded')
                        IS_OLD = 1
                    else:
                        IS_OLD = 0

                # If new people, speak with it, save the image in images folder and
                # write the name and corresponding object to Record.txt with the format of "name\tobject"

                if IS_OLD == 0 or IS_NEW == 1:
                    # Example:
                    # cv2.imwrite('./images/name.jpg', cv_image)
                    # gentleman, what's your name?
                    turtlebot_speak(0)
                    YES, nameflag, _, real_name = speak()
                    while not YES:
                        print("Please speak again, I didn't catch your name.")
                        YES, nameflag, _, real_name = speak()
                        notice_not1 = "Please speak again, I didn't catch your name."
                        synthesize_text(notice_not1, 4)
                    cv2.imwrite('./images/{}.jpg'.format(real_name), cv_image)
                    # Hi, XXX, nice to meet you ,what can i do for you?
                    turtlebot_speak(nameflag)
                    print("Listening: Please get me a banana/slipper/...")
                    YES, nameflag, objectflag, real_name = speak()
                    while not YES:
                        print("Please speak again, I didn't catch what you want.")
                        YES, nameflag, objectflag, real_name = speak()
                        notice_not2 = "Please speak again, I didn't catch what you want."
                        synthesize_text(notice_not2, 5)
                    print("Speaking: I'll get you the {}, wait for a moment".format(objectflag))
                    notice_is_object = "I'll get you the {}, wait for a moment".format(objectflag)
                    synthesize_text(notice_is_object, 6)
                    f = open("Record.txt", "w")
                    content = "{}\t{}".format(list_of_human[nameflag - 1], objectflag)
                    f.writelines(content)
                    DETECT_TIME = DETECT_TIME + 1
                # show the corresponding object to people
                if IS_OLD == 1:
                    pass
        else:
            print("No people in camera")

        if DETECT_TIME == 3:
            break
    return DETECT_TIME


def Human_compare():
    global Compared_name
    COMPARE_TIME = 0
    cap = cv2.VideoCapture(0)  # open the camera, parameter 0 if using the laptop
    while cap.isOpened():
        OK, frame = cap.read()
        if not OK:
            continue
        cv_image = frame
        result = Get_face_result(cv_image)
        if result is not None:
            draw_image, FACE_NUM, gender_list = Local_face(cv_image, True)  # Recognize people
            if FACE_NUM == 1:
                line_content = linecache.getline("Record.txt", 1)
                name1 = line_content.split('\t')[0]
                line_content = linecache.getline("Record.txt", 2)
                name2 = line_content.split('\t')[0]
                line_content = linecache.getline("Record.txt", 3)
                name3 = line_content.split('\t')[0]
                exist_img1 = cv2.imread('./images/' + name1 + '.jpg')
                exist_img2 = cv2.imread('./images/' + name2 + '.jpg')
                exist_img3 = cv2.imread('./images/' + name3 + '.jpg')
                IS_OLD_1 = Get_face_compare_result(exist_img1, cv_image)
                IS_OLD_2 = Get_face_compare_result(exist_img2, cv_image)
                IS_OLD_3 = Get_face_compare_result(exist_img3, cv_image)

                if IS_OLD_1 == -1 or IS_OLD_2 == -1 or IS_OLD_3 == -1:  # Request API fail !!!
                    continue

                if IS_OLD_1 == 1 or IS_OLD_2 == 1 or IS_OLD_3 == 1:
                    if IS_OLD_1 == 1:
                        name = name1
                    elif IS_OLD_2 == 1:
                        name = name2
                    else:
                        name = name3

                    for j in Compared_name:
                        if j == name:
                            IS_compared = 1
                            break
                    if IS_compared == 1:
                        print('The people has been compared')
                    else:
                        Compared_name.append(name)
                        Object = line_content.split('\t')[1].strip()
                        print("Speaking: Glad to see you again, {}, here's your {}.".format(name, object))
                        return_notice = "Speaking: Glad to see you again, {}, here's your {}.".format(name, object)
                        synthesize_text(return_notice, 15)

                        people_img = cv2.imread('./images/' + name + '.jpg')
                        Object_img = cv2.imread('./images/' + Object + '.jpg')
                        cv2.imshow(name, people_img)
                        cv2.imshow(Object, Object_img)
                        cv2.waitKey(500)
                        cv2.destroyAllWindows()
                        COMPARE_TIME = COMPARE_TIME + 1  # Record how many people has been Compared.

        if COMPARE_TIME == 3:
            break
    return COMPARE_TIME


if __name__ == '__main__':

    client = SocketClient(ip='127.0.0.1')
    face_mic = SocketClient()
    while 1:
        _, fn = face_mic.receiveFile()
        if fn == 'Human_detect.txt':
            while 1:
                DETECT_STATISTICS = Human_detect()
                if DETECT_STATISTICS == 3:
                    face_mic.sendFile('Record.txt')
                    break
            break
        else:
            continue

    while 1:
        received = multi_receive(client, save_path='../Face_mic/')
        if received:
            while 1:
                COMPARE_STATISTICS = Human_compare()
                if COMPARE_STATISTICS == 3:
                    break
            break
        else:
            continue

    print('---------------------------------Game over-------------------------------')