import cv2
import face_recognition
import os
import boto3
import pickle
import uuid
# Function to save known face encodings and labels
def save_known_faces(encodings, labels, filename):
    data = {'encodings': encodings, 'labels': labels}
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
        
def load_known_faces(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data['encodings'], data['labels']

os.environ['AWS_ACCESS_KEY_ID'] = 'your-localstack-access-key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-localstack-secret-key'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # Update with the desired region

# Set the LocalStack endpoint URL
localstack_endpoint_url = 'http://localhost:4566'  # Update with the correct LocalStack endpoint
# video_capture.release()
# cv2.destroyAllWindows()
video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera

new_faces_encodings = []
new_faces_labels = []
image_count = 0
unique_key = str(uuid.uuid4())
dynamodb = boto3.resource("dynamodb", endpoint_url=localstack_endpoint_url)
table_name = "gabrielmonzatorecord"
table = dynamodb.Table(table_name)
known_faces_file = 'known_faces.pkl'
known_face_encodings, known_face_labels = load_known_faces(known_faces_file)

while image_count < 40:
    ret, frame = video_capture.read()

    # Perform face detection on the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Add new faces to the dataset
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = f"Gabriel"
        new_faces_encodings.append(face_encoding)
        new_faces_labels.append(unique_key)
        image_count += 1

        # Display Results
        color = (0, 255, 0)  # Green rectangle for known faces
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, color, 1)

    cv2.imshow('Adding New Faces', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Save new faces to the existing dataset
known_face_encodings.extend(new_faces_encodings)
known_face_labels.extend(new_faces_labels)
save_known_faces(known_face_encodings, known_face_labels, known_faces_file)
table.put_item(
Item={
    'id': unique_key,
    'name': "Gabriel",
    'criminal_record': ["test"]
    }
                        )
video_capture.release()
cv2.destroyAllWindows()