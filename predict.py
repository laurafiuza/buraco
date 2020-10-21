import cv2
import tensorflow as tf
import pickle
from sklearn.metrics import confusion_matrix

CATEGORIES = ["with_mask", "without_mask", "mask_weared_incorrect"]

X_test = pickle.load(open("X_test.pickle", "rb"))
y_test = pickle.load(open("y_test.pickle", "rb"))

'''
IMG_SIZE = 50
img_array = cv2.imread("../../../../../Downloads/IMG_2578.jpg", cv2.IMREAD_GRAYSCALE)
print(img_array)
resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
reshaped = resized.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
'''

model = tf.keras.models.load_model("CNN.model")
predictions = model.predict(X_test)
predictions = [prediction.tolist().index(max(list(prediction))) for prediction in predictions]

print(confusion_matrix(predictions, y_test))
