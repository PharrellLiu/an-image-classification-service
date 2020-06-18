import time
import telepot
from telepot.loop import MessageLoop
from redis import StrictRedis
from multiprocessing import Pool

# Token
bot = telepot.Bot("919750665:AAF6RvEAEGPOPS77Q88MTguTW9sAfb3PM6Q")
# Get a connection to Redis
queueMsg = StrictRedis(host='localhost', port=6379)

processPool = Pool(3)


def downloadImage(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        content = msg["text"]
        print(content)
        print(time.localtime(time.time()))
        time.sleep(2)
        print(time.localtime(time.time()))


def handle(msg):
    processPool.apply_async(downloadImage(msg))
    # queueMsg.publish("receiveMsg", json.dumps(msg))


MessageLoop(bot, handle).run_as_thread()
# Keep the program running.
while 1:
    time.sleep(10)
