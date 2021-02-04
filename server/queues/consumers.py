import json

from django.core import serializers
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Queue, VirtualQueue
from .utils import predict_waittime, predict_total_waittime


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.queue = await self.get_queue()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'MSG':
            body = text_data_json['body']
            message = body['message']
            username = body['username']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_message',
                    'message': message,
                    'username': username,
                }
            )

        elif text_data_json['type'] == 'UPD':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_table',
                }
            )


    # * INFO:Actually not needed
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': 'MSG',
            'body':{
                'message': message,
                'username': username,
            }
        }))
    

    async def update_table(self, event):

        patient_queue = await self.get_patients_inqueue()
        print()
        data = json.dumps({
            'type': 'UPD',
            'body':{
                'queue': patient_queue
            }
        })
        await self.send(text_data=data)


    @database_sync_to_async
    def get_queue(self):
        return Queue.objects.filter(name=self.room_name).first()
    
    
    @database_sync_to_async
    def get_patients_inqueue(self):
        def format_model(item):
            nonlocal completion
            wait_time, completion = predict_waittime(item, completion)
            completed_at = item.completed_at 
            if completed_at:
                completed_at = True 
            return {
                'id': item.pk,
                'patient_id' : item.patient.pk,
                'patient_name': f"{item.patient.first_name} {item.patient.last_name}",
                'joined_at': f"{item.joined_at.hour}:{item.joined_at.minute}:{item.joined_at.second}",
                'completed_at' : completed_at , 
                'treatment_completed_at' : item.treatment_completed_at,
                'wait_time': wait_time,
                'position': item.get_patients_ahead(),
                'total_wait_time': predict_total_waittime(item)
                }
        
        completion = 12
        inqueue = self.queue.get_active_patients()
        inqueue = list(map(format_model, inqueue))
        return inqueue
