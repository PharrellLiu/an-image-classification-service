from redis import StrictRedis
from multiprocessing import Pool
import os
import time
import json


def ifImageExists(msg):
    data = json.loads(msg['data'])
    image_name = data['image_name']
    
    # if we cannot receive the image in 10 sec, we would consider it has failed
    count = 0
    while os.path.isfile(image_name) is False:
        if count >= 10:
            queue.publish("reply", json.dumps({'chat_id': data['chat_id'],
                                               'message': 'sorry, cannot download the image'}))
            return
        count += 1
        time.sleep(1)

    queue.publish("classify", msg['data'])


if __name__ == '__main__':
    queue = StrictRedis(host='localhost', port=6379)
    pubsub = queue.pubsub()
    pubsub.subscribe('image_check')

    # The first message you receive will be a confirmation of subscription
    message = pubsub.get_message()
    while message is None:
        message = pubsub.get_message()

    processPool = Pool()

    while True:
        message = pubsub.get_message()
        if message:
            processPool.apply_async(ifImageExists, args=(message,))
