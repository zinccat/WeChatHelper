# bot.py
from wechaty import Wechaty
import os
# import json
import csv

os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '127.0.0.1:9001'
os.environ['WECHATY_PUPPET_SERVICE_TOKEN']="change_to_your_padlocal_token into cat"

import asyncio
from typing import List, Optional, Union

from wechaty_puppet import FileBox  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

import json
from datetime import datetime

rootpath = './data'

def append_json(filename, message):
    if not os.path.exists(filename):
        initial_data = {
            "messages": [
                {
                }
            ]
        }
        with open(filename, 'w') as json_file:
            json.dump(initial_data, json_file)
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    data["messages"].append(message)
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
    return

def create_csv_file(file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User', 'Time', 'Text'])

def append_to_csv(file_name, user, text):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([user, current_time, text])

def get_name(contact):
    if contact.payload.alias.strip() != '':
        identity = contact.payload.alias
    elif contact.payload.name.strip() != '':
        identity = contact.payload.name
    else:
        identity = contact.contact_id
    return identity

class MyBot(Wechaty):

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact: Optional[Contact] = msg.talker()
        to_contact: Optional[Contact] = msg.to()
        text = msg.text()
        room: Optional[Room] = msg.room()

        if msg.message_type() != 6:
            return
        # if room is not None, save using room
        if room is not None:
            filename = rootpath+'/room/'+room.payload.topic+'.csv'
        else:
            # TODO:
            if to_contact.payload.name != "please change to your own wechat alias":
                filename = rootpath+'/user/'+get_name(to_contact)+'.csv'
            else:
                filename = rootpath+'/user/'+get_name(from_contact)+'.csv'
        # message = {
        #     "user": from_contact.payload.alias,
        #     "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        #     "text": text
        # }
        if not os.path.exists(filename):
            create_csv_file(filename)
        append_to_csv(filename, from_contact.name, text)


asyncio.run(MyBot().start())
