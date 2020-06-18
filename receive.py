import time
import telepot
from telepot.loop import MessageLoop
from redis import StrictRedis
import json

# Token
bot = telepot.Bot("919750665:AAF6RvEAEGPOPS77Q88MTguTW9sAfb3PM6Q")
# Get a connection to Redis
queueMsg = StrictRedis(host='localhost', port=6379)


def handle(msg):
    queueMsg.publish("receiveMsg", json.dumps(msg))


MessageLoop(bot, handle).run_as_thread()
# Keep the program running.
while 1:
    time.sleep(10)
