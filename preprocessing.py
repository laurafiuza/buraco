import numpy as np
import os
from matplotlib import pyplot as plt
import cv2
import random
import pickle
import xmltodict

DATA_DIR = "archive"

CATEGORIES = ["with_mask", "without_mask", "mask_weared_incorrect"]

IMG_SIZE = 50

training_data = []

images_path = os.path.join(DATA_DIR, "images")
for img in os.listdir(images_path):
    try:
        img_array = cv2.imread(os.path.join(images_path, img), cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        annotations_path = "archive/annotations/" + img[:-4] + ".xml"
        with open(annotations_path) as fd:
            info = xmltodict.parse(fd.read())
            label = info['annotation']['object']['name']
            training_data.append([resized, CATEGORIES.index(label)])
    except Exception as e:
        print(e)

random.shuffle(training_data)

X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

pickle_out = open('X.pickle', 'wb')
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open('y.pickle', 'wb')
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle", 'rb')
X = pickle.load(pickle_in)
