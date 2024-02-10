import cv2
import os
import numpy as np


def face_dector(image):
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    faces = faceCascade.detectMultiScale(
        image,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    img = image
    for (x,y,w,h) in faces:
      img =  image[y:y+h,x:x+w]
    return img 

    

def load_lfw_dataset(lfw_path):
    images = []
    labels = []
    label_dict = {}

    current_label = 0
    for person_name in os.listdir(lfw_path):
        person_path = os.path.join(lfw_path, person_name)
        if os.path.isdir(person_path):
            label_dict[current_label] = person_name

            for file_name in os.listdir(person_path):
                file_path = os.path.join(person_path, file_name)
                if file_name.endswith('.jpg'):
                    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                    img = face_dector(img)
                    cv2.imwrite("test/"+person_name+str(current_label)+".jpeg",img)
                    images.append(img)
                    labels.append(current_label)

            current_label += 1

    return images, labels, label_dict

def train_lbph_recognizer(images, labels):
    print(len(images))
    print(len(labels))
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, np.array(labels))
    return recognizer

def recognize_face(recognizer, test_image, label_dict):
    label, confidence = recognizer.predict(test_image)
    person_name = label_dict[label]
    return person_name, confidence

def main():
    lfw_path = '/Users/gabrielmonzato/Documents/kisame/model/data/lfw/lfw-deepfunneled/lfw-deepfunneled'  # Replace with the actual path to your LFW dataset
    test_image_path = '/Users/gabrielmonzato/Downloads/test.jpeg'  # Replace with the actual path to your test image

    images, labels, label_dict = load_lfw_dataset(lfw_path)
    # print(images)

    recognizer = train_lbph_recognizer(images, labels)

    test_image = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
    test_image=face_dector(test_image)
    person_name, confidence = recognize_face(recognizer, test_image, label_dict)
    cv2.imwrite("test/test_"+person_name+str(confidence)+".jpeg",test_image)

    print(f"Detected face belongs to: {person_name} with confidence: {confidence}")

if __name__ == "__main__":
    main()
