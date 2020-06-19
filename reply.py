import json
from multiprocessing import Pool

from redis import StrictRedis


def replyMessage(msg):
    data = json.loads(msg['data'])
    reply = data['message']
    chat_id = data['chat_id']



if __name__ == '__main__':
    queue = StrictRedis(host='localhost', port=6379)
    pubsub = queue.pubsub()
    pubsub.subscribe('reply')

    # The first message you receive will be a confirmation of subscription
    message = pubsub.get_message()
    while message is None:
        message = pubsub.get_message()

    processPool = Pool()
    while True:
        message = pubsub.get_message()
        if message:
            processPool.apply_async()
