#!/usr/bin/env python

from speech.text2speech import synthesize_text
from speech.emotion_analysis import requirements_meet
from speech.speechmain import speak
import linecache
from utils.tcp_client import SocketClient
from utils.multi_receive import multi_receive
import os
import face_recognition
import requests
from playsound import playsound
from human.face_detect import *
from human.face_compare_baidu import *
import cv2

# os.remove('./images/name.jpg')
# f = open('./Record.txt', 'r+')
# f.truncate()

list_of_human = ["John", "Jordan", "Tom"]

Compared_name = list()


# for list_name in range(3):
#     try:
#         os.remove('./images/{}.jpg'.format(list_of_human[list_name]))
#     except IOError:
#         print("FileNotFound Error: cannot find {}.jpg".format(list_of_human[list_name]))
#
# try:
#     f = open('./Record.txt', 'r+')
#     f.truncate()
# except IOError:
#     print("FileNotFound Error: cannot find Record.txt")


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


def Human_detect(face_mic):
    DETECT_TIME = 0
    # open the camera, parameter 0 if using the laptop
    while 1:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            OK, frame = cap.read()
            if not OK:
                continue
            cv_image = frame
            result = Get_face_result(cv_image)
            cv2.waitKey(1000)  # open api qps request limit reached
            cap.release()
            if result is not None:
                draw_image, FACE_NUM, gender_list = Local_face(cv_image, True)  # Recognize people
                if FACE_NUM == 1:
                    cv2.imshow('Recorded', draw_image)
                    cv2.waitKey(10)

                    # compare if it is the new people
                    file = open("Record.txt", "r")
                    content = file.readlines()
                    file.close()
                    IS_NEW = 0
                    IS_OLD = 0
                    if len(content) == 0:  # If the Record.txt is blank, the guy must be new.
                        IS_NEW = 1
                        print("IS_NEW = 1")
                    else:  # If the Record.txt is not blank, compare with other guy in Record.txt.
                        NAME_NUM = len(content)
                        IS_OLD_1 = 0
                        IS_OLD_2 = 0
                        IS_OLD_3 = 0
                        if NAME_NUM == 1:
                            name1 = content[0].split('\t')[0]
                            exist_img1 = cv2.imread('./images/' + name1 + '.jpg')
                            IS_OLD_1 = Get_face_compare_result(exist_img1, cv_image)
                        if NAME_NUM == 2:
                            name1 = content[0].split('\t')[0]
                            name2 = content[1].split('\t')[0]
                            exist_img1 = cv2.imread('./images/' + name1 + '.jpg')
                            exist_img2 = cv2.imread('./images/' + name2 + '.jpg')
                            IS_OLD_1 = Get_face_compare_result(exist_img1, cv_image)
                            IS_OLD_2 = Get_face_compare_result(exist_img2, cv_image)
                        if NAME_NUM == 3:
                            name1 = content[0].split('\t')[0]
                            name2 = content[1].split('\t')[0]
                            name3 = content[2].split('\t')[0]
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
                        # gentleman, what's your name?
                        turtlebot_speak(0)
                        YES, nameflag, _, real_name = speak()
                        while not YES:
                            print("Please speak again, I didn't catch your name.")
                            notice_not1 = "Please speak again, I didn't catch your name."
                            synthesize_text(notice_not1, 4)
                            YES, nameflag, _, real_name = speak()
                        print("Are you {}".format(real_name))
                        notice_conf_name = "Are you {}".format(real_name)
                        synthesize_text(notice_conf_name, 30)

                        cv2.imwrite('./images/{}.jpg'.format(real_name), cv_image)
                        # Hi, XXX, nice to meet you ,what can i do for you?
                        turtlebot_speak(nameflag)
                        print("Listening: Please get me a coffee/water/cookie...")
                        YES, _, objectflag, real_name = speak()
                        while not YES:
                            print("Please speak again, I didn't catch what you want.")
                            notice_not2 = "Please speak again, I didn't catch what you want."
                            synthesize_text(notice_not2, 5)
                            YES, _, objectflag, real_name = speak()
                        requirements_meet(objectflag)
                        print("Speaking: I'll get you the {}, wait for a moment".format(objectflag))
                        notice_is_object = ""
                        if objectflag == "iced_tea":
                            notice_is_object = "I'll get you the iced tea, wait for a moment"
                        else:
                            notice_is_object = "I'll get you the {}, wait for a moment".format(objectflag)
                        synthesize_text(notice_is_object, 6)
                        f1 = open("Record.txt", "a")
                        content = "{}\t{}\n".format(list_of_human[nameflag - 1], objectflag)
                        f1.writelines(content)
                        f1.close()
                        face_mic.sendFile('./images/{}.jpg'.format(list_of_human[DETECT_TIME]))
                        DETECT_TIME = DETECT_TIME + 1
                        # cap.release()
                    # show the corresponding object to people
                    if IS_OLD == 1:
                        pass
            else:
                print("No people in camera")

        if DETECT_TIME == 3:
            break
    return DETECT_TIME


def Human_compare():
    global Compared_name, IS_compared
    COMPARE_TIME = 0
    # cap = cv2.VideoCapture(0)  # open the camera, parameter 0 if using the laptop
    while 1:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            IS_compared = 0
            OK, frame = cap.read()
            if not OK:
                continue
            cv_image = frame
            result = Get_face_result(cv_image)
            cap.release()
            if result is not None:
                draw_image, FACE_NUM, gender_list = Local_face(cv_image, True)  # Recognize people
                if FACE_NUM == 1:
                    file = open("Record.txt", "r")
                    content = file.readlines()
                    file.close()
                    name1 = content[0].split('\t')[0]
                    print(name1)
                    name2 = content[1].split('\t')[0]
                    print(name2)
                    name3 = content[2].split('\t')[0]
                    print(name3)
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
                            Object_line = 0
                        elif IS_OLD_2 == 1:
                            name = name2
                            Object_line = 1
                        else:
                            name = name3
                            Object_line = 2
                        print(name)
                        for j in Compared_name:
                            if j == name:
                                IS_compared = 1
                                break
                        if IS_compared == 1:
                            print('The people has been compared')
                        else:
                            Compared_name.append(name)
                            print(Compared_name)
                            Object = content[Object_line].split('\t')[1].strip()
                            Object_img = cv2.imread('./images/' + Object + '.jpg')
                            people_img = cv2.imread('./images/' + name + '.jpg')
                            if Object_img is not None:
                                if Object == "iced_tea":
                                    Object1 = "iced tea"
                                    print("Speaking: Glad to see you again, {}, here's your {}.".format(name, Object1))
                                    return_notice = "Glad to see you again, {}, here's your {}.".format(name, Object1)
                                else:
                                    print("Speaking: Glad to see you again, {}, here's your {}.".format(name, Object))
                                    return_notice = "Glad to see you again, {}, here's your {}.".format(name, Object)
                                synthesize_text(return_notice, 15)
                                cv2.imshow(name, people_img)
                                cv2.imshow(Object, Object_img)
                            else:
                                print("Sorry {}, I cannot find what you want.".format(name))
                                ObjectFound = "Sorry {}, I cannot find the {}.".format(name, Object)
                                synthesize_text(ObjectFound, 20)
                                cv2.imshow(name, people_img)
                                # cv2.imshow(Object, Object_img)
                            cv2.waitKey(2000)
                            cv2.destroyAllWindows()
                            COMPARE_TIME = COMPARE_TIME + 1  # Record how many people has been Compared.

        if COMPARE_TIME == 3:
            break
    return COMPARE_TIME


if __name__ == '__main__':
    face_mic = SocketClient()

    while 1:
        _, fn = face_mic.receiveFile()
        if fn == 'Human_detect.txt':
            Human_detect(face_mic)
            face_mic.sendFile("Record.txt")
            break
        else:
            continue

    while 1:
        received = multi_receive(face_mic, save_path='./images/')
        if received:
            Human_compare()
            break
        else:
            continue

    print('---------------------------------Game over-------------------------------')
