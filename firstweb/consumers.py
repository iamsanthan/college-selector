import asyncio
import json
from . models import CoffeehouseUser,Thread,ChatMessage
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.room_group_name = 'chat_%s' % self.room_name
        print("connected",event)
        other_user=self.scope['url_route']['kwargs']['username']
        me=self.scope['user']
        print(me,self.scope['url_route']['kwargs']['username'])
        thread_obj=await self.get_thread(me,other_user)
        print(thread_obj)
        self.thread_obj=thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room=chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        # Join room group
        await self.send({
            "type": "websocket.accept",
            
        })
        

    # Receive message from
    async def websocket_receive(self, event):
        print("receive",event)
        front_text=event.get('text',None)
        if front_text is not None:
            loaded_dict_data=json.loads(front_text)
            msg=loaded_dict_data.get('message')
            user=self.scope['user']
            username='default'
            if user.is_authenticated:
                username=user.username
            myResponse={
                'message': msg,
                'username': username
            }
            await self.create_chat_message(user,msg)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )
        # Send message to room group
        

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        # Leave room group
        print("disconnected",event,'1')
        await self.send({
            "type": "websocket.disconnect",
            
        })

    @database_sync_to_async
    def get_thread(self,user,other_username):
        return Thread.objects.get_or_new(user,other_username)[0]

    @database_sync_to_async
    def create_chat_message(self,me,msg):
        thread_obj=self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj,user=me,message=msg)