from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("🟢 CONNECT CALLED")
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # 🔴 MUHIM: user authenticated bo‘lishi shart
        if self.scope["user"].is_anonymous:
            await self.close()
            return

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
        print("🔴 RECEIVE CALLED:", text_data)
        data = json.loads(text_data)
        message_text = data.get("message", "").strip()
        user = self.scope["user"]

        if not message_text:
            return

        # 🔴 CHATNI TO‘G‘RI OLISH
        chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)

        # 🔴 DB GA YOZISH (ENG MUHIM JOY)
        msg = await sync_to_async(Message.objects.create)(
            chat=chat,
            sender=user,
            text=message_text
        )

        # 🔴 chat updated_at ni yangilash
        chat.updated_at = msg.created_at
        await sync_to_async(chat.save)()

        # 🔴 BARCHAGA YUBORISH
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.text,
                "username": user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))
