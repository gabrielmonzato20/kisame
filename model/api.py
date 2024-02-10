from flask import Flask, request, jsonify
import cv2
import face_recognition
import boto3
import pickle
from datetime import datetime
import uuid
import os
from flask_cors import CORS  # Import the CORS module
import numpy as np 
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app, origins=["http://localhost:3002"])
print(app)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response
# Function to load known faces from a file
def load_known_faces(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data['encodings'], data['labels']

# Set up AWS credentials and S3 client
os.environ['AWS_ACCESS_KEY_ID'] = 'your-localstack-access-key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-localstack-secret-key'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # Update with the desired region

localstack_endpoint_url = 'http://localhost:4566'  # Update with the correct LocalStack endpoint
s3 = boto3.client("s3", endpoint_url=localstack_endpoint_url)

s3_bucket_name = 'gabrielmonzatovideoprocessor'
known_faces_file = 'known_faces.pkl'
dynamodb = boto3.resource("dynamodb", endpoint_url=localstack_endpoint_url)
table = dynamodb.Table('gabrielmonzatorecord')

if os.path.exists(known_faces_file):
    known_face_encodings, known_face_labels = load_known_faces(known_faces_file)

    @app.route('/process_video', methods=['POST'])
    def process_video():
        # Assuming video_data is a file in mp4 format
        video_file = request.files['video']

        # Save the video file to a temporary location
        video_filename = 'temp_video.mp4'
        video_file.save(video_filename)

        # Open the video using cv2.VideoCapture
        video_capture = cv2.VideoCapture(video_filename)

        frame_width = int(video_capture.get(3))
        frame_height = int(video_capture.get(4))

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        videoname = f'video_{timestamp}.mp4'
        video_writer = cv2.VideoWriter(videoname, cv2.VideoWriter_fourcc(*'avc1'), 30, (frame_width, frame_height))

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Perform face detection on the frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Unknown"
                if known_face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_labels[first_match_index]
                        response = table.get_item(Key={'id': name})
                        item = response.get('Item')
                        name = item["name"]
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, color, 1)

            # cv2.imshow('Video', frame)
            video_writer.write(frame)

        video_writer.release()
        unique_key = str(uuid.uuid4())
        with open(videoname, 'rb') as data:
            s3.upload_fileobj(data, s3_bucket_name, f'{unique_key}.mp4')
        os.remove(videoname)

        return jsonify({'message': 'Video processed and saved successfully'})


@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()

    if not data or 'frameData' not in data:
        return jsonify({'error': 'Missing or invalid frameData parameter'})

    frame_data = data['frameData']

    try:
        # Decode the base64 string into bytes
        image_bytes = base64.b64decode(frame_data)

        # Use BytesIO to create an in-memory binary stream
        image_stream = BytesIO(image_bytes)

        # Open the image using PIL (Python Imaging Library)
        image = Image.open(image_stream)

        # Convert the PIL image to a NumPy array
        frame_np = np.array(image, dtype=np.uint8)

        # Ensure the frame is not empty
        if frame_np is None or frame_np.size == 0:
            return jsonify({'error': 'Invalid image data'})

        # Perform face detection on the frame
        face_locations = face_recognition.face_locations(frame_np)
        face_encodings = face_recognition.face_encodings(frame_np, face_locations)

        result = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            records=[]
            if known_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_labels[first_match_index]
                    response = table.get_item(Key={'id': name})
                    item = response.get('Item',None)
                    name = item.get("name",name)
                    records = item.get("criminal_record",[])
            # Append the result for each face
            result.append({'name': name, 'box': {'top': top, 'right': right, 'bottom': bottom, 'left': left},"records":records})
        print(result)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Error processing frame: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True,port=5001)
