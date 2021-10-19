import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.layers import get_channel_layer
from .models import UserProfile

class ConnectToServer(AsyncWebsocketConsumer): # Primitive Connection to Mother server
    async def connect(self):

        self.chatroom = 'MAIN_SERVER'
        self.chatroom_group_name = f'chat_{self.chatroom}'


        await self.channel_layer.group_add(self.chatroom_group_name, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(self.chatroom_group_name,
            {
                'type': 'connected_to_server_message',
                'username': str(self.scope['user'])
            }
        )
        
    async def connected_to_server_message(self, event):

        username = event['username']

        await self.send(text_data=json.dumps({'content_type': 'USER_CONNECT_TO_SERVER', 'username': username}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chatroom_group_name, self.channel_name)
        await self.channel_layer.group_send(self.chatroom_group_name, {'type': 'disconnected_to_server_message', 'username': str(self.scope['user'])})

    async def disconnected_to_server_message(self, event):
        username = event['username']
        await self.send(text_data=json.dumps({'content_type': 'USER_DISCONNECT_FROM_SERVER', 'username': username}))



# class ChatRoomConsumer(AsyncWebsocketConsumer):

    '''
    async def connect(self):
        self.chatroom = self.scope['url_route']['kwargs']['chatroom']
        self.chatroom_group_name = 'chat_%s' % self.chatroom
        
        await self.channel_layer.group_add(self.chatroom_group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(self.chatroom_group_name,
            {
                'type': 'chatroom_joined_message',
                'username': str(self.scope['user'])
            }
        )

    async def chatroom_joined_message(self, event):
        
        username = event['username']

        await self.send(text_data=json.dumps({'content_type': 'USER_JOIN', 'username': username}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chatroom_group_name, self.channel_name)
        await self.channel_layer.group_send(self.chatroom_group_name, {'type': 'chatroom_left_message', 'username': str(self.scope['user'])})
    '''
    
#     async def chatroom_left_message(self, event):
#         username = event['username']
#         await self.send(text_data=json.dumps({'content_type': 'USER_LEFT', 'username': username}))

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         user = str(self.scope['user'])

#         await self.channel_layer.group_send(self.chatroom_group_name, {'type': 'chat_message', 'message': message, 'username': user})

#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']

#         await self.send(text_data=json.dumps({'content_type': 'USER_MESSAGE', 'message': message, 'username': username}))
    
