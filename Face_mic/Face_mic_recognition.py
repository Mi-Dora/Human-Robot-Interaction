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

list_of_human = ["John", "Jordan", "Tom"]
Compared_name = list()

for list_name in range(3):
    try:
        os.remove('./images/{}.jpg'.format(list_of_human[list_name]))
    except IOError:
        print("FileNotFound Error: cannot find {}.jpg".format(list_of_human[list_name]))

try:
    f = open('./Record.txt', 'r+')
    f.truncate()
except IOError:
    print("FileNotFound Error: cannot find Record.txt")

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
        cv2.waitKey(1000)  # open api qps request limit reached
        if result is not None:
            draw_image, FACE_NUM, gender_list = Local_face(cv_image, True)  # Recognize people
            if FACE_NUM == 1:
                cv2.imshow('test', draw_image)
                cv2.waitKey(100)

                # compare if it is the new people
                file = open("Record.txt", "r")
                content = file.read()
                IS_NEW = 0
                IS_OLD = 0
                known_encodings = []
                if len(content) == 0:  # If the Record.txt is blank, the guy must be new.
                    IS_NEW = 1
                    print("IS_NEW = 1")
                else:  # If the Record.txt is not blank, compare with other guy in Record.txt.
                    NAME_NUM = (len(open("Record.txt", 'rU').readlines()))
                    if NAME_NUM == 1:
                        line_content = linecache.getline("Record.txt", 1)
                        name1 = line_content.split('\t')[0]
                        known_person_1 = face_recognition.load_image_file('./images/' + name1 + '.jpg')
                        known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
                        known_encodings = [
                            known_person_1_encoding
                        ]
                    if NAME_NUM == 2:
                        line_content = linecache.getline("Record.txt", 1)
                        name1 = line_content.split('\t')[0]
                        known_person_1 = face_recognition.load_image_file('./images/' + name1 + '.jpg')
                        line_content = linecache.getline("Record.txt", 2)
                        name2 = line_content.split('\t')[0]
                        known_person_2 = face_recognition.load_image_file('./images/' + name2 + '.jpg')
                        known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
                        known_person_2_encoding = face_recognition.face_encodings(known_person_2)[0]
                        known_encodings = [
                            known_person_1_encoding,
                            known_person_2_encoding
                        ]
                    if NAME_NUM == 3:
                        line_content = linecache.getline("Record.txt", 1)
                        name1 = line_content.split('\t')[0]
                        known_person_1 = face_recognition.load_image_file('./images/' + name1 + '.jpg')
                        line_content = linecache.getline("Record.txt", 2)
                        name2 = line_content.split('\t')[0]
                        known_person_2 = face_recognition.load_image_file('./images/' + name2 + '.jpg')
                        line_content = linecache.getline("Record.txt", 3)
                        name3 = line_content.split('\t')[0]
                        known_person_3 = face_recognition.load_image_file('./images/' + name3 + '.jpg')
                        known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
                        known_person_2_encoding = face_recognition.face_encodings(known_person_2)[0]
                        known_person_3_encoding = face_recognition.face_encodings(known_person_3)[0]
                        known_encodings = [
                            known_person_1_encoding,
                            known_person_2_encoding,
                            known_person_3_encoding
                        ]
                    if len(face_recognition.face_encodings(cv_image)) > 0:
                        print("face found in image!")
                        unknown_person_encoding = face_recognition.face_encodings(cv_image)[0]
                    else:
                        print('Face Not found')
                        continue
                    face_distances = face_recognition.face_distance(known_encodings, unknown_person_encoding)
                    print("distance")
                    for i, face_distance in enumerate(face_distances):
                        print("Image has a distance of {:.2} from known image #{}".format(face_distance, i + 1))
                        if face_distance < 0.6:
                            line_content = linecache.getline("Record.txt", i + 1)
                            exist_name = line_content.split('\t')[0]
                            IS_OLD = 1
                            print(exist_name + ', you have been recorded')
                            break

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

                    cv2.imwrite('./images/{}.jpg'.format(real_name), cv_image)
                    # Hi, XXX, nice to meet you ,what can i do for you?
                    turtlebot_speak(nameflag)
                    print("Listening: Please get me a banana/slipper/...")
                    YES, _, objectflag, real_name = speak()
                    while not YES:
                        print("Please speak again, I didn't catch what you want.")
                        notice_not2 = "Please speak again, I didn't catch what you want."
                        synthesize_text(notice_not2, 5)
                        YES, _, objectflag, real_name = speak()

                    print("Speaking: I'll get you the {}, wait for a moment".format(objectflag))
                    notice_is_object = "I'll get you the {}, wait for a moment".format(objectflag)
                    synthesize_text(notice_is_object, 6)
                    f1 = open("Record.txt", "a")
                    content = "{}\t{}\n".format(list_of_human[nameflag - 1], objectflag)
                    f1.writelines(content)
                    f1.close()
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
                known_encodings = []
                if len(face_recognition.face_encodings(cv_image)) > 0:
                    print("face found in image!")
                    unknown_person_encoding = face_recognition.face_encodings(cv_image)[0]
                else:
                    print('Face Not found')
                    continue
                line_content = linecache.getline("Record.txt", 1)
                name1 = line_content.split('\t')[0]
                known_person_1 = face_recognition.load_image_file('./images/' + name1 + '.jpg')
                line_content = linecache.getline("Record.txt", 2)
                name2 = line_content.split('\t')[0]
                known_person_2 = face_recognition.load_image_file('./images/' + name2 + '.jpg')
                line_content = linecache.getline("Record.txt", 3)
                name3 = line_content.split('\t')[0]
                known_person_3 = face_recognition.load_image_file('./images/' + name3 + '.jpg')
                known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
                known_person_2_encoding = face_recognition.face_encodings(known_person_2)[0]
                known_person_3_encoding = face_recognition.face_encodings(known_person_3)[0]
                known_encodings = [
                    known_person_1_encoding,
                    known_person_2_encoding,
                    known_person_3_encoding
                ]
                face_distances = face_recognition.face_distance(known_encodings, unknown_person_encoding)
                IS_compared = 0
                for i, face_distance in enumerate(face_distances):
                    print("Image has a distance of {:.2} from known image #{}".format(face_distance, i + 1))
                    if face_distance < 0.6:
                        line_content = linecache.getline("Record.txt", i + 1)
                        name = line_content.split('\t')[0]
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
                            cv2.imshow(name, people_img)
                            Object_img = cv2.imread('./images/' + Object + '.jpg')
                            if Object_img is None:
                                print("Sorry sir, I cannot find what you want.")
                                ObjectFound = "Sorry sir, I cannot find the {}.".format(Object)
                                synthesize_text(ObjectFound, 20)
                            else:
                                cv2.imshow(Object, Object_img)
                            cv2.waitKey(500)
                            cv2.destroyAllWindows()
                            COMPARE_TIME = COMPARE_TIME + 1  # Record how many people has been Compared.

        if COMPARE_TIME == 3:
            break
    return COMPARE_TIME


if __name__ == '__main__':
    # Human_detect()
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
        received = multi_receive(client, save_path='./images/')
        if received:
            while 1:
                COMPARE_STATISTICS = Human_compare()
                if COMPARE_STATISTICS == 3:
                    break
            break
        else:
            continue

    print('---------------------------------Game over-------------------------------')