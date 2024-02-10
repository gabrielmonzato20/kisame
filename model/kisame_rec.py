import cv2
import face_recognition
import os
import boto3
import pickle
from datetime import datetime
import uuid
# Function to load known faces from a file
def load_known_faces(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data['encodings'], data['labels']

os.environ['AWS_ACCESS_KEY_ID'] = 'your-localstack-access-key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-localstack-secret-key'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
# Set the LocalStack endpoint URL
localstack_endpoint_url = 'http://localhost:4566'  # Update with the correct LocalStack endpoint

s3 = boto3.client("s3", endpoint_url=localstack_endpoint_url)

# S3 configuration
s3_bucket_name = 'gabrielmonzatovideoprocessor'

known_faces_file = 'known_faces.pkl'

if os.path.exists(known_faces_file):
    known_face_encodings, known_face_labels = load_known_faces(known_faces_file)

    # Video capture setup
    video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera

    # Video writer setup
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    videoname = f'video_{timestamp}.mp4'
    dynamodb = boto3.resource("dynamodb", endpoint_url=localstack_endpoint_url)
    table = dynamodb.Table('gabrielmonzatorecord')
    video_writer = cv2.VideoWriter(videoname, cv2.VideoWriter_fourcc(*'avc1'), 30, (frame_width, frame_height))

    while True:
        ret, frame = video_capture.read()

        # Perform face detection on the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Classify faces using known face encodings
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"

            if known_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_labels[first_match_index]
                    name = known_face_labels[first_match_index]
                    response = table.get_item(Key={'id': name})
                    item = response.get('Item')
                    name = item.get("name","nao achei")
            # Display Results
            color = (0, 255, 0)  # Green rectangle for known faces
            if name == "Unknown":
                color = (0, 0, 255)  # Red rectangle for unknown faces

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, color, 1)

        cv2.imshow('Video', frame)

        # Write frame to video file
        # video_writer.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Release the video writer and break the loop
            video_writer.release()

            # Generate timestamp for S3 object key
            unique_key = str(uuid.uuid4())


            # Upload the video file to S3 with timestamped key
            # with open(videoname, 'rb') as data:
            #     s3.upload_fileobj(data, s3_bucket_name, f'{unique_key}.mp4')
            #     print(unique_key)
            # # Optionally, you can delete the local video file after uploading
            # os.remove(videoname)

            break

else:
    print("Error:: Model not found")
