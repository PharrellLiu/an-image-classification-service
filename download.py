from redis import StrictRedis
import time
from multiprocessing import Pool
import telepot

# Connect and subscribe
queueMsg = StrictRedis(host='localhost', port=6379)
pubsubMsg = queueMsg.pubsub()
pubsubMsg.subscribe('receiveMsg')

# The first message you receive will be a confirmation of subscription
message = pubsubMsg.get_message()
while message is None:
    message = pubsubMsg.get_message()


def downloadImage(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        content = msg["text"]
        print(content)
        time.sleep(2)
        print('end')


processPool = Pool()
while True:
    message = pubsubMsg.get_message()
    if message:
        processPool.apply_async(downloadImage(message))
    else:
        time.sleep(1)
