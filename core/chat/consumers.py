import  json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Group, Message
from .serializers import MessageSerializer
from urllib.parse import parse_qs
from django.utils import timezone

from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def get_previous_group_messages(self, group_id):
        try:
            @database_sync_to_async
            def fetch_and_serialize_messages(group_id):
                messages = list(Message.objects.filter(group_id=group_id).order_by('timestamp'))
                serializer = MessageSerializer(messages, many=True)
                return serializer.data
            serialized_messages = await fetch_and_serialize_messages(group_id)

            return serialized_messages
        except Exception as e:
            return []

    @database_sync_to_async
    def create_chat(self, sender, msg, group_id=None):
        # Message.objects.get_or_create(sender_id=sender,content=msg,group_id=group_id, timestamp=timezone.now())
        message, created = Message.objects.get_or_create(
            sender_id=sender,
            content=msg,
            group_id=group_id,
            defaults={'timestamp': timezone.now()}  # Set timestamp as the default value
        )
        return message
    @database_sync_to_async
    def add_user_in_group(self,user_id, group_id):
        user_i = User.objects.get(id=user_id)
        g = Group.objects.get(id=group_id)
        g.members.add(user_i)
    @database_sync_to_async
    def get_user_detail(self, user_id):
        user = User.objects.get(pk=user_id)
        return user.first_name
    @database_sync_to_async
    def get_group(self,group_id):
        instance_of_group = Group.objects.get(id=group_id)
        return instance_of_group.name

    async def connect(self):
        await self.accept()

        query_string = self.scope.get('query_string', b'').decode('utf-8')
        query_parameters = parse_qs(query_string)
        self.group_id = self.scope["url_route"]["kwargs"]['group_name']
        self.group_name = await self.get_group(self.group_id)

        self.user_id = query_parameters.get('user_id', [None])[0]

        await self.add_user_in_group(self.user_id, self.group_id)

        if self.user_id:
            self.user_first_name = await self.get_user_detail(self.user_id)
            previous_messages = await self.get_previous_group_messages(self.group_id)
            for message in previous_messages:
                # print(message['recipient'])
                if not message['recipient']:
                    data = {
                        "sender": message['sender'],
                        "message": json.loads(message['content'])['message'],
                        "full_name": message['first_name'],
                    }
                    await self.send(text_data=json.dumps(data))

            await self.channel_layer.group_add(self.group_name, self.channel_name)
        else:
            await self.close(code=1008)  # Close the connection if user_id is not provided


    async def receive(self, text_data=None, bytes_data=None):
        if self.user_id:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": text_data,
                    "user_id": self.user_id,  # Pass the user_id along with the message
                    "full_name": f'{self.user_first_name}',
                },
            )

    async def chat_message(self, event):
        if self.user_id:
            sender_id = event.get("user_id")
            message_text = event.get("message")
            if sender_id and message_text:
                await self.create_chat(sender_id, message_text, self.group_id)
                await self.send(text_data=json.dumps({
                    "sender": sender_id,
                    "message": json.loads(event["message"])['message'],
                    "full_name": event.get("full_name"),
                }))