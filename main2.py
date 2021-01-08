#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import os
import vk_api
from vk_api import VkUpload
import requests
from bs4 import BeautifulSoup
import time


login, password = 'ЛогинВк', 'ПарольВК'
channel = "КаналТГбез@"
owner_id = "ВашЧисловойIDвк"
text = "ТекстСзаписью,например#anime"

vk_session = vk_api.VkApi(login, password)
vk_session.auth()
lastnum = 0
while True:
    url = 'https://rsshub.app/telegram/channel/'+channel
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features='xml')
    items = soup.find('item')
    upload = VkUpload(vk_session)
    lastcount = str(items.contents[9].next)[str(items.contents[9].next).find(channel)+len(channel)+1:]
    print(lastcount)
    try:
        if lastnum != lastcount:
            lastnum = lastcount
            item = items
            l = str(item.description)
            URL = l[l.find('"') + 1:l.find('jpg') + 3]
            filename = 'pic/jk.jpg'
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
                'owner_id': '-' + owner_id,
                'message': text,
                'attachment': attachment,
            })
            os.remove(photos)
            print("Отправил новое фото")
        else:
            print("Нет новых фото в rss")
        time.sleep(3600)
    except LookupError:
        print("Нет пикч")
        time.sleep(3600)
