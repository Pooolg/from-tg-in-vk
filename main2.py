#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import os
import vk_api
from vk_api import VkUpload
import requests
from bs4 import BeautifulSoup
import time
login, password = 'ЛогинВК', 'ПарольВк'
app_id = '7719267'
vk_session = vk_api.VkApi(login, password, app_id)       #можно использовать авторизацию через токен приложения, читать документацию vk_api
vk_session.auth()
g=0
while g == 0:
    url = 'https://rsshub.app/telegram/channel/sad_art_gallery'     #Вместо "sad_art_gallery" вписывайте любой публичный канал, откуда нужно сграбить пикчи
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features='xml')
    items = soup.find_all('item')
    score = 0
    upload = VkUpload(vk_session)
    for i in range(len(items)):
        item = items[i]
        l = str(item.description)
        URL = l[l.find('"') + 1:l.find('jpg') + 3]
        score = score + 1
        filename = 'pic/jk' + str(score) + '.jpg'
        response = requests.get(URL)
        if response.status_code == 200:
            with open(filename, 'wb') as imgfile:
                imgfile.write(response.content)
        directory = 'pic//'
        files = os.listdir(directory)
        files = [i for i in files if i.endswith('.jpg')]
        photos = (directory + random.choice(files))
        photo_list = upload.photo_wall(photos)
        attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
        vk_session.method("wall.post", {
            'owner_id': '-193504246',            # id вашего сообщества в ВКонтакте
            'message': '#anime',                 # текст поста
            'attachment': attachment,
        })
        os.remove(photos)
        time.sleep(3600)                         № интервал между публикациями
