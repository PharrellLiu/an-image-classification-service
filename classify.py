from multiprocessing import Pool
import requests
import torch
import torchvision.models as models
from PIL import Image
from redis import StrictRedis
from torch.autograd import Variable
import torchvision.transforms as transforms
import json


def imageClassify(msg):
    data = json.loads(msg['data'])
    image_name = data['image_name']
    chat_id = data['chat_id']

    image = Image.open(image_name)
    img_tensor = preprocess(image)
    img_tensor.unsqueeze_(0)
    img_variable = Variable(img_tensor)

    model.eval()

    preds = model(img_variable)

    percentage = torch.nn.functional.softmax(preds, dim=1)[0]
    predictions = []
    for i, score in enumerate(percentage.data.numpy()):
        predictions.append((score, labels[str(i)][1]))

    predictions.sort(reverse=True)

    result = ''
    count = 0
    for score, label in predictions[:5]:
        count += 1
        result = result + label + ' : ' + str(score)
        if count < 5:
            result += '\n'

    queue.publish("reply", json.dumps({'chat_id': chat_id,
                                       'message': result}))

    queue.publish("garbage", image_name)


if __name__ == "__main__":
    queue = StrictRedis(host='localhost', port=6379)
    pubsub = queue.pubsub()
    pubsub.subscribe('classify')

    message = pubsub.get_message()
    while message is None:
        message = pubsub.get_message()

    # prepare for the inception v3 model
    model = models.inception_v3(pretrained=True)
    model.transform_input = True

    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(299),
        transforms.ToTensor(),
        normalize
    ])
    content = requests.get(
        "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json").text
    labels = json.loads(content)

    print("model's ready")

    processPool = Pool()
    while True:
        message = pubsub.get_message()
        if message:
            processPool.apply_async(imageClassify, args=(message,))
