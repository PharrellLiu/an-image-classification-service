import time
from multiprocessing import Pool
import os
processPool = Pool(3)


def downloadImage():
    print(time.localtime(time.time()))
    print(os.getpid())
    time.sleep(3)
    print(time.localtime(time.time()))


for i in range(10):
    processPool.apply_async(downloadImage())
processPool.join()