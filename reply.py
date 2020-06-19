import json
from multiprocessing import Pool
import telepot
from redis import StrictRedis


def replyMessage(msg):
    data = json.loads(msg['data'])
    reply = data['message']
    chat_id = data['chat_id']
    bot.sendMessage(chat_id, reply)


if __name__ == '__main__':
    queue = StrictRedis(host='localhost', port=6379)
    pubsub = queue.pubsub()
    pubsub.subscribe('reply')

    message = pubsub.get_message()
    while message is None:
        message = pubsub.get_message()

    bot = telepot.Bot("***** PUT YOUR TOKEN HERE *****")

    processPool = Pool()

    while True:
        message = pubsub.get_message()
        if message:
            processPool.apply_async(replyMessage, args=(message,))
