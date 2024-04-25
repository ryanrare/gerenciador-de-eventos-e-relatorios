import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

active_consumers = []


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        active_consumers.append(self)

    def disconnect(self, close_code):
        active_consumers.remove(self)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #tratar alguns dados aqui
