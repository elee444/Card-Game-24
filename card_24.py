"""
Card Recognition using OpenCV
based on the code from the blog post
http://arnab.org/blog/so-i-suck-24-automating-card-games-using-opencv-and-python

Usage:

  ./card_img.py input_filename

Example:
  ./card_img.py input

Note: The recognition method is not very robust; please see SIFT / SURF for a good algorithm.

"""
#!/usr/bin/python3
import sys
import numpy as np
#sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")
import cv2
#import string
from post_24 import compute
import time
import csv


###############################################################################
# Utility code from
# http://git.io/vGi60A
# Thanks to author of the sudoku example for the wonderful blog posts!
###############################################################################

def rectify(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)


    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h, axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

###############################################################################
# Image Matching
###############################################################################


def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 1)
    return thresh


def imgdiff(img1, img2):
    img1 = cv2.GaussianBlur(img1, (5, 5), 5)
    img2 = cv2.GaussianBlur(img2, (5, 5), 5)
    diff = cv2.absdiff(img1, img2)
    diff = cv2.GaussianBlur(diff, (5, 5), 5)
    flag, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY)
    return np.sum(diff)


def find_closest_card(training, img):
    features = preprocess(img)
    return sorted(
        training.values(),
        key=lambda x: imgdiff(
            x[1],
            features))[0][0]


###############################################################################
# Card Extraction
###############################################################################
def getCards(im, numcards=4):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)

#  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    _, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:numcards]

    for card in contours:
        peri = cv2.arcLength(card, True)
        approx = rectify(cv2.approxPolyDP(card, 0.02 * peri, True))

#        if __name__ == '__main__':
#            box = np.int0(approx)
#            cv2.drawContours(im,[box],0,(255,255,0),6)
#            imx = cv2.resize(im,(1000,600))
#            cv2.imshow('a',imx)
#            cv2.waitKey(0)
#           cv2.destroyAllWindows()


        h = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)
        #Affine transformation
        transform = cv2.getPerspectiveTransform(approx, h)
        warp = cv2.warpPerspective(im, transform, (450, 450))
        yield warp


def get_training(
        training_labels_filename,
        training_image_filename,
        num_training_cards,
        avoid_cards=None):

    training = {}
    labels = {}

#  for line in file(training_labels_filename):
#    key, num, suit = line.strip().split()
#    labels[int(key)] = (num,suit)
    print("Reading training images")
    start_time = time.clock()
    with open(training_labels_filename, newline='') as fp:
        reader=csv.DictReader(fp,delimiter='\t')
        
        for i,row in enumerate(reader):
#            print(row['Key'],row['Num'],row['Suit'])
             key_ = str(row['Key'])
             num_ = str(row['Num'])
             suit_= str(row['Suit'])
             labels[int(key_)] = (num_, suit_)
             
#             print(i,key_,labels[int(key_)])
    
    """
        with open(training_labels_filename) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            key_, num_, suit_ = line.strip().split()
            labels[int(key_)] = (num_, suit_)
            line = fp.readline()
            cnt += 1
    """
    print("Done reading")
    print("--- %s seconds ---" % (time.clock() - start_time))
    fp.close()
    print("Training")
    start_time = time.clock()
    im = cv2.imread(training_image_filename)
    for i, c in enumerate(getCards(im, num_training_cards)):
        cv2.imwrite(labels[i][0]+labels[i][1]+".jpg",c)
        if avoid_cards is None or (
                labels[i][0] not in avoid_cards[0] and labels[i][1] not in avoid_cards[1]):
            training[i] = (labels[i], preprocess(c))

    print("Done training!!!!!!!!!!")
    print("--- %s seconds ---" % (time.clock() - start_time))
    return training

# Main


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infp:
            infp.readline()  # line 1 is the description of the file
            infpargv = infp.readline().strip().split(' ')

            #print(infpargv)
            filename = infpargv[0]
            num_cards = int(infpargv[1])
            training_image_filename = infpargv[2]
            training_labels_filename = infpargv[3]
            num_training_cards = int(infpargv[4])

        training = get_training(
            training_labels_filename,
            training_image_filename,
            num_training_cards)

        im = cv2.imread(filename)

        """
        width = im.shape[0]
        height = im.shape[1]
        if width < height:
            im = cv2.transpose(im)
            im = cv2.flip(im, 1)
        """
        # Debug: uncomment to see registered images
        for i,c in enumerate(getCards(im,num_cards)):
            width = im.shape[0]
            height = im.shape[1]
            if width < height:
                im = cv2.transpose(im)
                im = cv2.flip(im, 1)
            card = find_closest_card(training,c,)
            cv2.imshow(str(card),c)
            cv2.waitKey(0)

        cards = [
            find_closest_card(
                training,
                c) for c in getCards(
                im,
                num_cards)]
        print(cards)
        xlist=[]
        for x,_ in cards:
            x=str(x)
            if (x =="A"):
                xlist.append("1")
            elif (x in "12345678910"):
                xlist.append(x)
            else:
                print("Invaild card!")
                quit()
        compute(xlist)

    else:
        print(__doc__)

