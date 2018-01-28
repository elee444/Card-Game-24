import sys
import numpy as np
#sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")
import cv2
#import string
from post_24 import compute
import time
from card_24 import getCards

training_image_filename='test3.png'
num_training_cards=4
im = cv2.imread(training_image_filename)


for i, c in enumerate(getCards(im, num_training_cards)):
    width = im.shape[0]
    height = im.shape[1]
    if width < height:
        im = cv2.transpose(im)
        im = cv2.flip(im, 1)
    cv2.imshow(str(i),c)
    cv2.waitKey(0)
    


