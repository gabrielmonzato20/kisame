import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
import matplotlib.pyplot as plt

# Load the trained model
model = load_model('face_recognition_model.h5')

# Load and preprocess the test image
image_path = '/Users/gabrielmonzato/Downloads/test.jpeg'  # Replace with the actual path to your image
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (96, 96))  # Resize the image to match the model's input size

# Display the original test image
cv2.imshow('Test Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Preprocess the test image
test_data = img.reshape((1, 96, 96, 1))
test_data = test_data.astype("float32") / 255.0
plt.imshow(test_data[0, :, :, 0], cmap='gray')
plt.title('Preprocessed Image')
plt.show()

# # Make predictions
# predictions = model.predict(test_data)

# # Assuming your model is trained for binary classification (2 classes)
# # Replace this part based on your actual model output and class labels
# class_labels = []
# for person_name in os.listdir('data/lfw/lfw-deepfunneled/lfw-deepfunneled'):
#     person_path = os.path.join('data/lfw/lfw-deepfunneled/lfw-deepfunneled', person_name)
#     if os.path.isdir(person_path):
#         class_labels.append(person_name)

# # Label encoding
# label_encoder = {label: i for i, label in enumerate(class_labels)}

# # Decode the predictions
# predicted_class = np.argmax(predictions[0])
# predicted_label = [label for label, idx in label_encoder.items() if idx == predicted_class][0]

# print(f"Predicted Class: {predicted_class}, Predicted Label: {predicted_label}")
