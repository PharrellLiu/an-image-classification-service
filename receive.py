import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from redis import StrictRedis
import time
import json


class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self.queue = StrictRedis(host='localhost', port=6379)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'photo':
            image_name = str(chat_id) + time.strftime("%H:%M:%S", time.localtime()) + '.png'
            await bot.download_file(msg['photo'][-1]['file_id'], image_name)
            self.queue.publish("image_check", json.dumps({'chat_id': chat_id, 'image_name': image_name}))
        elif content_type == 'text':
            image_url = msg["text"]
            self.queue.publish("image_request", json.dumps({'chat_id': chat_id, 'image_url': image_url}))
        else:
            await self.sender.sendMessage("do not accept it, photo or url please")


TOKEN = '919750665:AAF6RvEAEGPOPS77Q88MTguTW9sAfb3PM6Q'

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=100),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
loop.run_forever()
