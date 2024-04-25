import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(
            text_data=json.dumps({
                "type": "conexao estabeleciada",
                "message": "notificação conectada com sucesso!"
            })
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #tratar alguns dados aqui

        print('Message', message)
        self.send(
            text_data=json.dumps({
                'type': 'chat',
                'message': message
            })
        )



    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
