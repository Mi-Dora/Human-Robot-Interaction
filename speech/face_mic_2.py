#!/usr/bin/env python
# license removed for brevity
from speech.text2speech import synthesize_text
from speech.speechmain import speak
import linecache
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
import face_recognition
import requests
from playsound import playsound
from human.face_detect import *


def Face_mic(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        cv_image = cv2.imread()
        cv2.waitKey(3000)
        result = Get_face_result(cv_image)
        cv2.waitKey(3000)

        if result != None:
            draw_image, FACE_NUM, gender_list = Local_face(cv_image, True)
            if FACE_NUM == 1:
                cv2.imshow('test', draw_image)
                cv2.waitKey(100)
                # detect if it is the new people
                file = open("/home/alan/catkin_ws/label.txt", "r")
                content = file.read()
                NEW = 0
                FOUND = 0
                known_encodings = []
                if len(content) == 0:
                    NEW = 1
                    print("NEW = 1")
                else:
                    NAME_NUM = (len(open("/home/alan/catkin_ws/label.txt", 'rU').readlines())) / 2  # num of name
                    if NAME_NUM == 1:
                        line_content = linecache.getline("/home/alan/catkin_ws/label.txt", 1)
                        name1 = line_content.split(' ')[0]
                        known_person_1 = face_recognition.load_image_file(name1 + ".jpg")
                        known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
                        known_encodings = [
                            known_person_1_encoding
                        ]
                    if NAME_NUM == 2:
                        line_content = linecache.getline("/home/alan/catkin_ws/label.txt", 1)
                        name1 = line_content.split(' ')[0]
                        known_person_1 = face_recognition.load_image_file(name1 + ".jpg")
                        line_content = linecache.getline("/home/alan/catkin_ws/label.txt", 2)
                        name2 = line_content.split(' ')[0]
                        known_person_2 = face_recognition.load_image_file(name2 + ".jpg")
                        known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
                        known_person_2_encoding = face_recognition.face_encodings(known_person_2)[0]
                        known_encodings = [
                            known_person_1_encoding,
                            known_person_2_encoding
                        ]
                    if NAME_NUM == 3:
                        line_content = linecache.getline("/home/alan/catkin_ws/label.txt", 1)
                        name1 = line_content.split(' ')[0]
                        known_person_1 = face_recognition.load_image_file(name1 + ".jpg")
                        line_content = linecache.getline("/home/alan/catkin_ws/label.txt", 2)
                        name2 = line_content.split(' ')[0]
                        known_person_2 = face_recognition.load_image_file(name2 + ".jpg")
                        line_content = linecache.getline("/home/alan/catkin_ws/label.txt", 3)
                        name3 = line_content.split(' ')[0]
                        known_person_3 = face_recognition.load_image_file(name3 + ".jpg")
                        known_person_1_encoding = face_recognition.face_encodings(known_person_1)[0]
                        known_person_2_encoding = face_recognition.face_encodings(known_person_2)[0]
                        known_person_3_encoding = face_recognition.face_encodings(known_person_3)[0]
                        known_encodings = [
                            known_person_1_encoding,
                            known_person_2_encoding,
                            known_person_3_encoding
                        ]
                    unknown_person_encoding = face_recognition.face_encodings(cv_image)[0]
                    face_distances = face_recognition.face_distance(known_encodings, unknown_person_encoding)
                    for i, face_distance in enumerate(face_distances):
                        print(
                            "The test image has a distance of {:.2} from known image #{}".format(face_distance, i + 1))
                        if face_distance < 0.6:
                            line_content = linecache.getline("/home/alan/catkin_ws/label.txt", i + 1)
                            exist_name = line_content.split(' ')[0]
                            FOUND = 1
                            print('Your are ' + exist_name)
                            break

                # If it is the new people, interact with it.
                if FOUND == 0 or NEW == 1:
                    if gender_list[0] == "male":
                        print("gentleman, what is your name?")
                        notice_gentleman = "gentleman, what is your name?"
                        synthesize_text(notice_gentleman, 1)
                    else:
                        print("Lady, what is your name?")
                        notice_lady = "Lady, what is your name?"
                        synthesize_text(notice_lady, 2)
                    print("Listening: My name is alan")
                    YES = speak()
                    if YES:
                        print("Speaking: Is that your name is alan?")
                        notice_isAlan = "Is that your name is alan?"
                        synthesize_text(notice_isAlan, 3)
                    else:
                        print("Please speak again, I didn't catch your name.")
                        notice_not1 = "Please speak again, I didn't catch your name."
                        synthesize_text(notice_not1, 4)
                    print("Listening: Yes")
                    YES = speak()
                    if YES:
                        cv2.imwrite("/home/alan/catkin_ws/alan.jpg", cv_image)
                    else:
                        print("Speaking: Please speak again, yes or not?")
                        notice_not2 = "Please speak again, yes or not?"
                        synthesize_text(notice_not2, 5)

                    print("Speaking : Hey alan, what can i do for you?")
                    notice_Alanhelp = "Hey alan, what can i do for you?"
                    synthesize_text(notice_Alanhelp, 6)
                    print("Listening: Banana")
                    YES = speak()
                    if YES:
                        print("Speaking: Is that banana?")
                        notice_Isbanana = "Is that banana?"
                        synthesize_text(notice_Isbanana, 7)
                    else:
                        print("Please speak again, what is it?")
                        notice_not3 = "Please speak again, what is it?"
                        synthesize_text(notice_not3, 8)
                    print("Listening: Yes")
                    YES = speak()
                    if YES:
                        f = open("/home/alan/catkin_ws/label.txt", "w")
                        content = "alan\tbanana"
                        f.writelines(content)
                    else:
                        print("Speaking: Please speak again, yes or not?")
                        playsound("output{}.mp3".format(5))

                # show the thing to people
                if FOUND == 1:
                    pass
        else:
            print("No people in camera")
    except CvBridgeError as e:
        print(e)


if __name__ == '__main__':
    Face_mic()
