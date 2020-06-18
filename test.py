import os
import random
import time
from multiprocessing import Pool
from redis import StrictRedis


def long_time_task():
    print('Run task (%s)...' % (os.getpid()))
    start = time.time()
    time.sleep(1)
    end = time.time()
    print('Task runs %0.2f seconds.' % (end - start))


if __name__ == '__main__':
    '''print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task)

    while 1:
        time.sleep(10)'''
    # Connect and subscribe
    queue = StrictRedis(host='localhost', port=6379)
    pubsub = queue.pubsub()
    pubsub.subscribe('testing')
    # The first message you receive will be a confirmation of subscription
    message = pubsub.get_message()
    print("The first message received:")
    print(message)
    p = Pool()
    while True:
        message = pubsub.get_message()
        if message:
            p.apply_async(long_time_task)
