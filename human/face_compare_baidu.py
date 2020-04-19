# encoding:utf-8

import requests
import base64
import json
import cv2


def Cv2_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str


def read_img(img1, img2):
    with open(img1, 'rb') as f:
        pic1 = base64.b64encode(f.read())
    with open(img2, 'rb') as f:
        pic2 = base64.b64encode(f.read())
    params = json.dumps([
        {"image": str(pic1, "utf-8"), "image_type": 'BASE64', "face_type": "LIVE"},
        {"image": str(pic2, "utf-8"), "image_type": 'BASE64', "face_type": "LIVE"}
    ])
    return params


def Get_face_compare_result(Aim_img, New_img):
    # Get access_token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=hXgjFGBG3B0gHUhy8PcYetDq&client_secret=uyQgI1zkU9yzkUPCKnXug22xEkXMDWuc'
    response = requests.get(host)
    if response:
        json1 = response.json()  # <class 'dict'>
        access_token = json1['access_token']
    else:
        print('Get access_token fail!')
        return -1
    # Compare two picture
    img1 = Cv2_base64(Aim_img)
    img2 = Cv2_base64(New_img)
    params = json.dumps([
        {"image": str(img1, "utf-8"), "image_type": 'BASE64', "face_type": "LIVE"},
        {"image": str(img2, "utf-8"), "image_type": 'BASE64', "face_type": "LIVE"}
    ])
    # params = read_img(Aim_img, New_img)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        face_compare_score = response.json()['result']['score']
        if face_compare_score > 80:
            return 1
        else:
            print('Not the same guy')
            return 0
    else:
        print('Get result fail!')
        return -1
