#!/usr/bin/env python

# from speech.text2speech import synthesize_text
# from speech.speechmain import speak
import linecache
import cv2
import face_recognition
import requests
from playsound import playsound
from human.face_detect import *

cap = cv2.VideoCapture('http://192.168.0.3:4747/video')  # open the camera, parameter 0 if using the laptop
while cap.isOpened():
    OK, frame = cap.read()
    if not OK:
        continue
    cv_image = frame
    result = Get_face_result(cv_image)
    #cv2.waitKey(1000)  # open api qps request limit reached
    if result is not None:
        draw_image, FACE_NUM, gender_list = Local_face(cv_image, True)   # Recognize people
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
            ########################## Code here ########################################
            if IS_OLD == 0 or IS_NEW == 1:
                # Example:
                cv2.imwrite('./images/name.jpg', cv_image)
                f = open("Record.txt", "w")
                content = "name\tbanana"
                f.writelines(content)
            ############################################################################

            # show the corresponding object to people
            if IS_OLD == 1:
                pass
    else:
        print("No people in camera")


