from urllib import request
from redis import StrictRedis
from multiprocessing import Pool
from PIL import Image
import time
import json
import socket

# for the timeout, but i am not sure that it is useful or not
socket.setdefaulttimeout(30)


def requestImage(msg):
    data = json.loads(msg['data'])
    image_url = data['image_url']
    chat_id = data['chat_id']
    image_name = str(chat_id) + time.strftime("%H:%M:%S", time.localtime()) + '.png'

    retries = 3
    while retries > 0:
        try:
            request.urlretrieve(image_url, image_name)
            break
        except Exception as e:
            print(e)
            if retries == 1:
                queue.publish("reply", json.dumps({'chat_id': chat_id,
                                                   'message': 'sorry, cannot download anything from the url'}))
                return
            retries -= 1
            continue

    # check if the file is an image or not
    try:
        image = Image.open(image_name)
    except IOError:
        queue.publish("reply", json.dumps({'chat_id': chat_id,
                                           'message': 'it is not an image'}))
        queue.publish("garbage", image_name)
        return

    queue.publish("classify", json.dumps({'chat_id': chat_id,
                                          'image_name': image_name}))


if __name__ == '__main__':
    queue = StrictRedis(host='localhost', port=6379)
    pubsub = queue.pubsub()
    pubsub.subscribe('image_request')

    # The first message you receive will be a confirmation of subscription
    message = pubsub.get_message()
    while message is None:
        message = pubsub.get_message()

    processPool = Pool()

    while True:
        message = pubsub.get_message()
        if message:
            processPool.apply_async(requestImage, args=(message,))
