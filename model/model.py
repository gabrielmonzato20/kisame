import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
# Load the LFW dataset
def load_lfw_dataset():
    data = []
    labels = []
    for person_name in os.listdir('data/lfw/lfw-deepfunneled/lfw-deepfunneled'):
        person_path = os.path.join('data/lfw/lfw-deepfunneled/lfw-deepfunneled', person_name)
        if os.path.isdir(person_path):
            for file_name in os.listdir(person_path):
                file_path = os.path.join(person_path, file_name)
                if file_name.endswith('.jpg'):
                    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (96, 96))  # Resize the image to a fixed size
                    data.append(img)
                    labels.append(person_name)

    return np.array(data), np.array(labels)

# Preprocess the data and labels
def preprocess_data(data, labels):
    data = data.reshape((data.shape[0], 96, 96)).astype("float32") * 255.0
    data = data.astype(np.uint8)
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels = to_categorical(labels)

    return data, labels

# Build a simple face recognition model
def build_model():
    # base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(96, 96, 3))
    # base_model.trainable = False
    # model = Sequential([
    #     layers.Rescaling(1./255, input_shape=(96, 96, 1)),
    #     layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(32, (3,3), padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(64, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Flatten(),
    #     layers.Dense(128, activation='relu'),
    #     layers.Dense(5749)
    #     ])

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(96, 96, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(5749, activation='softmax'))  # Adjust the number of units based on the number of classes

    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    return model

# Train the model
def train_model(model, data, labels):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    history = model.fit(
        X_train,
        y_train,
        epochs=20,
        # batch_size=32,
        # validation_data=(X_test, y_test),
        # callbacks=[early_stopping]
    )

    return model, history

# Main function
def main():
    data, labels = load_lfw_dataset()
    data, labels = preprocess_data(data, labels)

    # # Convert grayscale images to RGB
    # data = np.repeat(data, 3, axis=-1)

    model = build_model()

    trained_model, history = train_model(model, data, labels)

    # Save the model
    trained_model.save('face_recognition_model.h5')

if __name__ == "__main__":
    main()
