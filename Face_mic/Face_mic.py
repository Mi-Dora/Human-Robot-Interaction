#!/usr/bin/env python

from speech.text2speech import synthesize_text
from speech.speechmain import speak
import linecache
import os
import cv2
import face_recognition
import requests
from playsound import playsound
from human.face_detect import *

# os.remove('./images/name.jpg')
# f = open('./Record.txt', 'r+')
# f.truncate()

list_of_human = ["David", "Jordan", "Lebron"]

DETECT_TIME = 0
COMPARE_TIME = 0
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
    global DETECT_TIME
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


def Human_compare():
    global Compared_name
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
                            Object = line_content.split('\t')[1]

                            #######################################################################################
                            ####################################### Code here #####################################
                            ###
                            ###  Task: Speaking the name and the corresponding object above
                            ###  etc: print('Speaking: Glad to see you again, alan(name), This is your (object) ')
                            ###
                            #######################################################################################
                            #######################################################################################

                            people_img = cv2.imread('./images/' + name + '.jpg')
                            Object_img = cv2.imread('./images/' + Object + '.jpg')
                            cv2.imshow(name, people_img)
                            cv2.imshow(Object, Object_img)
                            cv2.waitKey(500)
                            cv2.destroyAllWindows()
                            COMPARE_TIME = COMPARE_TIME + 1  # Record how many people has been Compared.

        if COMPARE_TIME == 3:
            break


def client():  # Receive the message from TCP Server
    pass


if __name__ == '__main__':

    # while 1:
    #     client()                              #Waiting receive the Human_detect message
    #     if message == "Human_detect":         #once get the message ,break
    #         break

    while 1:
        Human_detect()
        if DETECT_TIME == 3:
            break

    # while 1:
    #     client()                              #Waiting receive the Human_compare message
    #     if message == "Human_compare":        #once get the message ,break
    #         break

    while 1:
        Human_compare()
        if COMPARE_TIME == 3:
            break

    print('Game over')
