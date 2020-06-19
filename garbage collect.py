import os
from redis import StrictRedis

if __name__ == '__main__':
    queue = StrictRedis(host='localhost', port=6379)
    pubsub = queue.pubsub()
    pubsub.subscribe('garbage')

    message = pubsub.get_message()
    while message is None:
        message = pubsub.get_message()

    while True:
        message = pubsub.get_message()
        if message:
            image_name = bytes.decode(message['data'])
            if os.path.isfile(image_name):
                os.remove(image_name)
            else:
                pass
