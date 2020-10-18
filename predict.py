import cv2
import tensorflow as tf

CATEGORIES = ["with_mask", "without_mask", "mask_weared_incorrect"]

IMG_SIZE = 50
img_array = cv2.imread("../../../../../Downloads/IMG_2578.jpg", cv2.IMREAD_GRAYSCALE)
print(img_array)
resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
reshaped = resized.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

model = tf.keras.models.load_model("CNN.model")
prediction = model.predict([reshaped])
prediction = list(prediction[0])
print(prediction)
print(CATEGORIES[prediction.index(max(prediction))])
