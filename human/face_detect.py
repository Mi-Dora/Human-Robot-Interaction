#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:17:22 2020

@author: alanby  zhihaibi90@gmail.com
"""

import requests
import base64
import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2


def Cv2_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str


def Get_face_result(cv2_img):
    # get access_token; client_id is AK, client_secret is SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=1WHQrZiBNubCSxYfdBTgev1j&client_secret=YnI7nVIIFa5wG2z0lonkgTGamVCuvI1Q'
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    response1 = requests.post(url=host, headers=header)  # <class 'requests.models.Response'>
    json1 = response1.json()  # <class 'dict'>
    access_token = json1['access_token']
    base64_img = Cv2_base64(cv2_img)  # Transform

    # face_api
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {"image": base64_img, "image_type": "BASE64", "face_field": "age,gender,face_shape,", "max_face_num": "10"}
    header = {'Content-Type': 'application/json'}
    request_url = request_url + "?access_token=" + access_token
    response1 = requests.post(url=request_url, data=params, headers=header)  # <class 'requests.models.Response'>
    if len(response1.json()) == 6:
        face_result = response1.json()['result']
        return face_result
    else:
        return None


def Get_face_locations(face_result):
    face_num = face_result['face_num']
    face_list = face_result['face_list']
    face_locations = []
    face_location = []
    for i in range(face_num):
        face_loaction_dic = face_list[i]['location']
        # top, right, bottom, left
        face_location.append(int(face_loaction_dic['top']))
        face_location.append(int(face_loaction_dic['left'] + face_loaction_dic['width']))
        face_location.append(int(face_loaction_dic['top'] + face_loaction_dic['height']))
        face_location.append(int(face_loaction_dic['left']))
        face_locations.append((tuple(face_location)))
        face_location.clear()
    # print(face_locations)
    return face_locations


def Get_gender_list(face_result):
    face_num = face_result['face_num']
    face_list = face_result['face_list']
    gender_list = []
    for i in range(face_num):
        gender_dic = face_list[i]['gender']
        gender_list.append(gender_dic['type'])
    print(gender_list)
    return gender_list


def Local_face(cv2_img, selection):
    result = Get_face_result(cv2_img)
    face_locations = Get_face_locations(result)
    gender_list = Get_gender_list(result)
    face_num = len(face_locations)
    if (face_num > 0):
        for i in range(face_num):
            top, right, bottom, left = face_locations[i]
            gender = gender_list[i]
            draw_image = cv2.rectangle(cv2_img, (left, top), (right, bottom), (0, 0, 255), 2)
            if (selection == True):  # Marking Num & gender
                cv2.putText(draw_image, str(i + 1) + ' ' + gender, (left, bottom), cv2.FONT_HERSHEY_TRIPLEX, 0.6,
                            (0, 255, 0), 1)
        return draw_image, face_num, gender_list
    return False, 0, 0
