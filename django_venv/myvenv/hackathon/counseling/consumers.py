import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            # Online.objects.create(
            #     user=user,
            #     channel_name=self.channel_name,
            #     time=timezone.now()
            # )
            self.accept()

    def disconnect(self, close_code):
        # Online.objects.filter(channel_name=self.channel_name).delete()
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        _type = text_data_json['type']
        if _type == 'apply':
            packet = {
                'type': _type,
                'counselee': {
                    'name': self.scope['user'].username,
                    'channel_name': self.channel_name
                },
                'reason': text_data_json['reason']
            }
        elif _type == 'accept_counsel':
            packet = {
                'type': _type,
                'opponent': self.channel_name
            }
        elif _type == 'message':
            packet = {
                'type': _type,
                'opponent': {
                    'name': self.scope['user'].username,
                    'channel_name': self.channel_name
                },
                'message': text_data_json['message']
            }

        async_to_sync(self.channel_layer.send)(self.channel_name, {
            'type': _type,
            'packet': packet,
        })

    def apply(self, event):
        self.send(json.dumps(event['packet']))

    def accept_counsel(self, event):
        self.send(json.dumps(event['packet']))
    
    def message(self, event):
        self.send(json.dumps(event['packet']))