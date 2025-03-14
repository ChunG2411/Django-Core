from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class SignalsConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'signals'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        try:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    "type": "signals",
                    "data": data_json['data']
                }
            )
        except Exception as e:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'signals',
                    'data': None
                }
            )

    def signals(self, e):
        self.send(text_data=json.dumps(e, default=str))
