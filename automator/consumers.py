import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import time, math
from .models import UserProfile
from chat.models import Chat, Message

class MotherServer(AsyncWebsocketConsumer): # Primitive Connection to Mother Server
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            return None


        self.chatroom = 'MAIN_SERVER'
        self.chatroom_group_name = f'chat_{self.chatroom}'


        await self.channel_layer.group_add(self.chatroom_group_name, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(self.chatroom_group_name,
            {
                'type': 'connected_to_server_message',
                'user': self.scope['user']
            }
        )
        
        await self.mark_online(self.scope['user'])

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chatroom_group_name, self.channel_name)
        await self.channel_layer.group_send(self.chatroom_group_name, 
            {
                'type': 'disconnected_to_server_message',
                'user': self.scope['user']
            }
        )

        await self.mark_offline(self.scope['user'])

    async def receive(self, text_data): # async def receive(self, text_data=None, bytes_data=None):
        
        '''
        BASE FORMAT OF SOCKET JSON 'MESSAGE'
        {   
            "__ID__": int(math.modf(time.time() * 1000)[1]),
            "__TYPE__": <'CHAT_MESSAGE'/'CHAT_MESSAGE_STATUS'/...>,
            "CONTENT": {

                # For 'CHAT_MESSAGE' ----------------------

                "CHAT_ID": 45,
                "MESSAGE": {
                    "TEXT": 'watcha doin mate?',
                    "AUTHOR": <username>,
                }

                # For 'CHAT_MESSAGE_STATUS' ----------------------(SERVER - Response)

                "CHAT_ID": 45,
                "MESSAGE": {
                    "SUCCESS": True, # or False
                    "ERRORS": [],
                }

                # For ...            ----------------------

                ...


            },
        }

        '''

        text_data_json = json.loads(text_data)
        CLIENT_MESSAGE = text_data_json['__MESSAGE__']
        CLIENT_MESSAGE_ID = CLIENT_MESSAGE['__ID__']
        user = self.scope['user']

        if CLIENT_MESSAGE['__TYPE__'] == 'CHAT_MESSAGE':
            content = CLIENT_MESSAGE['CONTENT']

            chat_id = content['CHAT_ID']
            message = content['MESSAGE']
            
            message_text = message['TEXT']

            # Manipulate DB
            
            SUCCESS = True
            
            s = await self.addmessage2chat(chat_id, message_text, user) # Created Message

            if not s[1]:
                SUCCESS = False

            RESPONSE_JSON = {   
                "__ID__": CLIENT_MESSAGE_ID,
                "__TYPE__": 'CHAT_MESSAGE_STATUS',
                "CONTENT": {

                    "MESSAGE_ID": s[0],
                    "MESSAGE": {
                        "AUTHOR": self.scope['user'].username,
                        "TIME_SENT": s[3],
                        "SUCCESS": SUCCESS,
                        "ERRORS": s[2],
                }


                },
            }

            # SEND RESPONSE to SENDER
            await self.send(text_data=json.dumps(RESPONSE_JSON))

            if SUCCESS:
                pass # Send that down the chat group





        # print(CLIENT_MESSAGE)
        # print(user)
        
        # await self.channel_layer.group_send(self.chatroom_group_name, {'type': 'chat_message', 'message': message, 'username': user})


    '''
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({'content_type': 'USER_MESSAGE', 'message': message, 'username': username}))
    '''


    # MADE UP

    # ASYNC def(s):

    async def connected_to_server_message(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({'content_type': 'USER_CONNECT_TO_SERVER', 'username': user.username}))

    async def disconnected_to_server_message(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({'content_type': 'USER_DISCONNECT_FROM_SERVER', 'username': user.username}))



    # SYNC def(s):
    @database_sync_to_async
    def mark_online(self, user):
        u = UserProfile.objects.get(user=user)
        u.online = True
        u.save()

    @database_sync_to_async
    def mark_offline(self, user):
        u = UserProfile.objects.get(user=user)
        u.online = False
        u.save()


    @database_sync_to_async
    def addmessage2chat(self, chat_id, message_text, author):
        try:
            chat = Chat.objects.get(id=chat_id)
            msg = Message.objects.create(message=message_text, chat=chat, author=author)
            return (chat.id, True, [], msg.time_sent.strftime("%H:%m %d.%m.%y")) # (chat id, success or not, errors, message time_sent)
        except Exception:
            return (None, False, [str(Exception)], None) #Success or Now
            
        





'''
class ChatRoomConsumer(AsyncWebsocketConsumer):

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
    
    async def chatroom_left_message(self, event):
        username = event['username']
        await self.send(text_data=json.dumps({'content_type': 'USER_LEFT', 'username': username}))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = str(self.scope['user'])

        await self.channel_layer.group_send(self.chatroom_group_name, {'type': 'chat_message', 'message': message, 'username': user})

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({'content_type': 'USER_MESSAGE', 'message': message, 'username': username}))
    

'''

# class NotificationsManager(AsyncWebsocketConsumer):
#     async def connect(self):
#         pass
