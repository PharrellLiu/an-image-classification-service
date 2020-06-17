import time
import telepot
from telepot.loop import MessageLoop


bot = telepot.Bot("919750665:AAF6RvEAEGPOPS77Q88MTguTW9sAfb3PM6Q")


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'photo':
        bot.download_file(msg['photo'][-1]['file_id'], 'file.png')


if __name__ == "__main__":

    MessageLoop(bot, handle).run_as_thread()
    while 1:
        time.sleep(10)
