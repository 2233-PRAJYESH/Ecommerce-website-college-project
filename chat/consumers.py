import json

from django.db.models import Q
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

from .models import Chat, Message, User, GroupChat, GroupMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Set the users who chat with each other
        self.user1 = self.scope['user']
        self.user2 = int(self.scope['url_route']['kwargs']['room_name'])
        self.user2 = await self.get_user(self.user2)

        self.chat_id = await self.get_chat_id(self.user1, self.user2)

        self.messages = await self.fetch_messages(self.chat_id)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.chat_id}"
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        
        await self.send(text_data=json.dumps(self.messages))
    
    async def disconnect(self, code):
        return super().disconnect(code)
    
    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.save_message(self.chat_id, message, self.user1)

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "chat_id": self.chat_id.id,
                "message_content": message,
                "sender": self.user1.username
            }
        )

    async def chat_message(self, event):
        chat_id = event["chat_id"]
        message = event["message_content"]
        sender = event["sender"]
        await self.send(text_data=json.dumps(
            {
                "chat_id": chat_id,
                "message_content": message,
                "sender": sender,
                "timestamp": str(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
            }
        ))
    
    # Fetches past messages if any
    # Returns an array of dictionaries containing Message object details
    @database_sync_to_async
    def fetch_messages(self, chat_id):
        messages = Message.objects.filter(chat_id=chat_id)
        msg = []
        for message in messages:
            item = {}
            item['chat_id'] = message.chat_id.id
            item['message_content'] = message.message_content
            item['sender'] = message.sender.username
            item['timestamp'] = message.timestamp.strftime("%Y-%m-%d %I:%M %p")
            msg.append(item)
        return msg
    
    # Saves incoming messages to the database
    @database_sync_to_async
    def save_message(self, chat_id, message_content, sender):
        message = Message(chat_id=chat_id, message_content=message_content, sender=sender)
        message.save()
    
    # Fetches Chat ID of the current chat
    # Returns <class 'chat.models.Chat'> object
    @database_sync_to_async
    def get_chat_id(self, user1, user2):
        if user1.id > user2.id:
            user1, user2 = user2, user1
        elif user1.id == user2.id:
            raise ValueError("Invalid input")

        try:
            chat = Chat.objects.get(
                Q(user1=user1) & Q(user2=user2)
            )
        except ValueError:
            self.close()
        except:
            chat = Chat(user1=user1, user2=user2)
            chat.save()

        return chat
    
    # This function is used to fetch User object
    # Returns <class 'django.contrib.auth.models.User'> object
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

###########################################################################

# Logic for group chat consumer
class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        self.group_name = self.scope['url_route']['kwargs']['group_name']

        self.room_group_name = f"chat_{self.group_name}"

        self.chat_id = await self.get_chat_id(self.group_name)

        self.messages = await self.fetch_messages(self.chat_id)

        # Join channels group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        await self.send(text_data=json.dumps(self.messages))
    
    async def disconnect(self, code):
        return await super().disconnect(code)
        
    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.save_message(self.chat_id, message, self.user)

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "chat_id": self.chat_id.group_id,
                "message_content": message,
                "sender": self.user.username
            }
        )

    async def chat_message(self, event):
        chat_id = event["chat_id"]
        message = event["message_content"]
        sender = event["sender"]
        await self.send(text_data=json.dumps(
            {
                "chat_id": chat_id,
                "message_content": message,
                "sender": sender,
                "timestamp": str(datetime.now().strftime("%Y-%m-%d %I:%M %p"))
            }
        ))

    # Fetches past messages if any
    # Returns an array of dictionaries containing Message object details
    @database_sync_to_async
    def fetch_messages(self, chat_id):
        messages = GroupMessage.objects.filter(chat_id=chat_id)
        msg = []
        for message in messages:
            item = {}
            item['chat_id'] = message.chat_id.group_id
            item['message_content'] = message.message_content
            item['sender'] = message.sender.username
            item['timestamp'] = message.timestamp.strftime("%Y-%m-%d %I:%M %p")
            msg.append(item)
        return msg

    # Saves incoming messages to the database
    @database_sync_to_async
    def save_message(self, chat_id, message_content, sender):
        message = GroupMessage(chat_id=chat_id, message_content=message_content, sender=sender)
        message.save()
    
    @database_sync_to_async
    def get_chat_id(self, group_name):
        group = GroupChat.objects.get(group_name=group_name)
        return group