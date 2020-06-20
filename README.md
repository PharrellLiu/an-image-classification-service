# an image classification service

Introduction

So, this is a small image classification service, the idea is from the assignments and content of one of my course, 
it is about machine learning and how to deploy machine learning. This service is naive, it would not be useful, just like the assignments of courses, only for learning and practicing. Anyway, it has some defects, some errors, if you wanna issue me, please. Again, don't take it seriously, I am just a fresh grad, 
looking for a job and hoping this could impress the interviewer (that is impossible) or at least show something of me (LOL).

About It

Let's talk about the entirety first. I use a telegram bot as a port, users send image, or image's URL to the bot, and then receive the result on it too. And I use the PyTorch Inception V3 model to classify the image (I have to say the result is totally bad, 
and the initiation is slow, but the focus point is not the ML model!). 

These are the basic stuff, besides these, I use Redis's pub/sub as the way of communication between the processes, also 
use the multiprocess to achieve parallel processing. 

Now let me introduce the code.

receive.py: To receive the users' messages. If the message is the photo, the bot would download it. If this is text, the program would consider it as a URL, receive it too. If this is other things, the program would not accept it and reply "don't accept" to the user.

file check for bot download.py: Since I use async_download the photo in receive.py if the message is a photo, the program needs to make sure that the image has been downloaded before classification. This is to check whether the image has been downloaded successfully.

request image from url.py:  If the message is text, this program would be used. Try to request the resource from the URL, and 
after acquiring something, check if it is an image, not other stuff.

classify.py: the machine learning model is here, so I don't talk more about it.

reply.py: All the reply messages would be sent in here.

garbage collect.py: This is a good one! after downloading something and using it, this program would delete it immediately, 
but still, this function has some defects, it cannot delete all the downloaded things in some situations.

Something Tricky

The async model of telepot is so hard to understand! Anyway, I just put the URL here, you guys can have a look at it. https://telepot.readthedocs.io/en/latest/

In The End

I wanted to deploy it on the AWS EC2, but I failed since the free instance type only has 1 GB memory, I cannot install the torch package on it, the package is too large. But I think these programs can be deployed easily if the memory is enough. And, we can use the Supervisor to control this service.
