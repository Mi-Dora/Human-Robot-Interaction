# -*- coding: UTF-8 -*-
from aip import AipSpeech
# from playsound import playsound
from pygame import mixer
import time
import random
import os


def broadcast(text):
    APP_ID = '19503332'
    API_KEY = '5udk4rpl64MGuHMrgb068fxI'
    SECRET_KEY = 'DXGksTQTSzHrgu8g9LkM3FqPptRALjbv'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result = client.synthesis(text, 'zh', 1, {'vol': 5, 'spd': 3, 'pit': 5, 'per': 0})
    file_name = str(int(time.time())) + ".mp3"
    if not isinstance(result, dict):
        with open(file_name, 'wb') as f:
            f.write(result)

    mixer.init()
    mixer.music.load(file_name)
    mixer.music.play()
    time.sleep(5)
    mixer.music.stop()
    os.remove(file_name)

if __name__ == '__main__':
    broadcast("龟龟正在前往寻找物品")
