import os
import cv2
import face_recognition


def load_lfw_dataset(lfw_path):
    known_faces = {}
    for person_name in os.listdir(lfw_path):
        person_path = os.path.join(lfw_path, person_name)
        if os.path.isdir(person_path):
            known_faces[person_name] = []
            for file_name in os.listdir(person_path):
                file_path = os.path.join(person_path, file_name)
                if file_name.endswith('.jpg'):
                    known_faces[person_name].append(file_path)
    return known_faces

def compute_face_encodings(image_paths):
    face_encodings = []
    for image_path in image_paths:
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Detect faces using MTCNN
        detector = MTCNN()
        faces = detector.detect_faces(rgb_image)
        
        # Extract face encodings using face_recognition
        for face in faces:
            x, y, w, h = face['box']
            face_image = rgb_image[y:y+h, x:x+w]
            face_location = [(y, x + w, y + h, x)]

            print(face_image)
            face_descriptor = face_recognition.face_encodings(face_image,known_face_locations=face_location)
            if face_encoding:
                face_encodings.append(face_encoding[0])
    return face_encodings

def main():
    lfw_path = '/Users/gabrielmonzato/Documents/kisame/model/data/lfw/lfw-deepfunneled/lfw-deepfunneled'  # Replace with the actual path to your LFW dataset
    test_image_path = '/Users/gabrielmonzato/Downloads/test.jpg'  # Replace with the actual path to your test image

    known_faces = load_lfw_dataset(lfw_path)

    known_face_encodings = {}
    for person_name, image_paths in known_faces.items():
        known_face_encodings[person_name] = compute_face_encodings(image_paths)

    test_image = cv2.imread(test_image_path)
    test_rgb_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
    print("test_rgb_image")
    # Detect faces using MTCNN
    detector = MTCNN()
    faces = detector.detect_faces(test_rgb_image)

    # Extract face encodings using face_recognition
    test_face_encodings = []
    for face in faces:
        x, y, w, h = face['box']
        face_image = test_rgb_image[y:y+h, x:x+w]
        face_encoding = face_recognition.face_encodings(face_image)
        if face_encoding:
            test_face_encodings.append(face_encoding[0])

    # Compare the detected faces with known faces
    for person_name, person_encodings in known_face_encodings.items():
        for test_encoding in test_face_encodings:
            matches = face_recognition.compare_faces(person_encodings, test_encoding)
            if True in matches:
                print(f"Detected face belongs to: {person_name}")
                break
        else:
            continue
        break
    else:
        print("Detected face does not match any known person.")

    # Display the result
    for face in faces:
        x, y, w, h = face['box']
        cv2.rectangle(test_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Face Recognition', test_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
