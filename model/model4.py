import cv2
import face_recognition
import os
import boto3
import pickle
os.environ['AWS_ACCESS_KEY_ID'] = 'your-localstack-access-key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-localstack-secret-key'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # Update with the desired region
# Initialize S3 and DynamoDB clients
# Set the LocalStack endpoint URL
localstack_endpoint_url = 'http://localhost:4566'  # Update with the correct LocalStack endpoint

s3 = boto3.client("s3", endpoint_url=localstack_endpoint_url)


# Function to save known face encodings and labels
def save_known_faces(encodings, labels, filename):
    data = {'encodings': encodings, 'labels': labels}
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

# Function to load known face encodings and labels
def load_known_faces(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data['encodings'], data['labels']

# Step 1: Dataset Preparation
s3_bucket_name = 'gabrielmonzatorawimage12321'
known_faces_file = 'known_faces.pkl'

if os.path.exists(known_faces_file):
    known_face_encodings, known_face_labels = load_known_faces(known_faces_file)
else:
    known_face_encodings = []
    known_face_labels = []
    count = 0
    # List objects in S3 bucket

        
    paginator = s3.get_paginator('list_objects_v2')  
    pages = paginator.paginate(Bucket=s3_bucket_name)
    for page in pages:
        for obj in page['Contents']:
                image_key = obj['Key']
                label = os.path.splitext(os.path.basename(image_key))[0]

                # Download image from S3
                response = s3.get_object(Bucket=s3_bucket_name, Key=image_key)
                img = face_recognition.load_image_file(response['Body'])

                # Face recognition
                face_encodings = face_recognition.face_encodings(img)
                count+=1
                print(count)

                if face_encodings:  # Check if any faces were detected
                    known_face_encodings.append(face_encodings[0])
                    known_face_labels.append(label)

print("Saving ")
print(f"size:{len(known_face_encodings)} , {len(known_face_labels)}")
save_known_faces(known_face_encodings, known_face_labels, known_faces_file)
# # Function to save known face encodings and labels
# def save_known_faces(encodings, labels, filename):
#     data = {'encodings': encodings, 'labels': labels}
#     with open(filename, 'wb') as file:
#         pickle.dump(data, file)
# # Function to load known face encodings and labels
# def load_known_faces(filename):
#     with open(filename, 'rb') as file:
#         data = pickle.load(file)
#     return data['encodings'], data['labels']
# # Step 1: Dataset Preparation
# dataset_path = '/Users/gabrielmonzato/Documents/kisame/model/data/lfw/lfw-deepfunneled/lfw-deepfunneled'
# known_faces_file = 'known_faces.pkl'

# if os.path.exists(known_faces_file):
#     known_face_encodings, known_face_labels = load_known_faces(known_faces_file)
# else:
#     known_face_encodings = []
#     known_face_labels = []

#     labels = os.listdir(dataset_path)
#     for label in labels:
#         label_path = os.path.join(dataset_path, label)
#         if os.path.isdir(label_path):
#             for image_name in os.listdir(label_path):
#                 image_path = os.path.join(label_path, image_name)
#                 if image_name.endswith('.jpg') or image_name.endswith('.png'):
#                     img = face_recognition.load_image_file(image_path)
#                     face_encodings = face_recognition.face_encodings(img)
#                     print(label)
#                     if face_encodings:  # Check if any faces were detected
#                         known_face_encodings.append(face_encodings[0])
#                         known_face_labels.append(label)
#     print("Saving ")
#     save_known_faces(known_face_encodings, known_face_labels, known_faces_file) 











# s3 = boto3.client("s3")
# # Function to save known face encodings and labels
# def save_known_faces(encodings, labels, filename):
#     data = {'encodings': encodings, 'labels': labels}
#     with open(filename, 'wb') as file:
#         pickle.dump(data, file)
# # Function to load known face encodings and labels
# def load_known_faces(filename):
#     with open(filename, 'rb') as file:
#         data = pickle.load(file)
#     return data['encodings'], data['labels']
# # Step 1: Dataset Preparation
# dataset_path = '/Users/gabrielmonzato/Documents/kisame/model/data/lfw/lfw-deepfunneled/lfw-deepfunneled'
# known_faces_file = 'known_faces.pkl'

# if os.path.exists(known_faces_file):
#     known_face_encodings, known_face_labels = load_known_faces(known_faces_file)
# else:
#     known_face_encodings = []
#     known_face_labels = []

#     labels = os.listdir(dataset_path)
#     for label in labels:
#         label_path = os.path.join(dataset_path, label)
#         if os.path.isdir(label_path):
#             for image_name in os.listdir(label_path):
#                 image_path = os.path.join(label_path, image_name)
#                 if image_name.endswith('.jpg') or image_name.endswith('.png'):
#                     img = face_recognition.load_image_file(image_path)
#                     face_encodings = face_recognition.face_encodings(img)
#                     print(label)
#                     if face_encodings:  # Check if any faces were detected
#                         known_face_encodings.append(face_encodings[0])
#                         known_face_labels.append(label)
#     print("Saving ")
#     save_known_faces(known_face_encodings, known_face_labels, known_faces_file)




# # video_capture.release()
# # cv2.destroyAllWindows()
# video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera

# new_faces_encodings = []
# new_faces_labels = []
# image_count = 0

# while image_count < 40:
#     ret, frame = video_capture.read()

#     # Perform face detection on the frame
#     face_locations = face_recognition.face_locations(frame)
#     face_encodings = face_recognition.face_encodings(frame, face_locations)

#     # Add new faces to the dataset
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         name = f"Gabriel"
#         new_faces_encodings.append(face_encoding)
#         new_faces_labels.append(name)
#         image_count += 1

#         # Display Results
#         color = (0, 255, 0)  # Green rectangle for known faces
#         cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, color, 1)

#     cv2.imshow('Adding New Faces', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Save new faces to the existing dataset
# known_face_encodings.extend(new_faces_encodings)
# known_face_labels.extend(new_faces_labels)
# save_known_faces(known_face_encodings, known_face_labels, known_faces_file)

# video_capture.release()
# cv2.destroyAllWindows()