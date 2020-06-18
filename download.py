from redis import StrictRedis
import time

# Connect and subscribe
queueMsg = StrictRedis(host='localhost', port=6379)
pubsubMsg = queueMsg.pubsub()
pubsubMsg.subscribe('receiveMsg')

# The first message you receive will be a confirmation of subscription
message = pubsubMsg.get_message()
while message is None:
    message = pubsubMsg.get_message()

while True:
    message = pubsubMsg.get_message()
    if message:
        print(message)
    else:
        time.sleep(1)
