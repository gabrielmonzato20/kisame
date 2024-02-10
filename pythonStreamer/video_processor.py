# video_processor.py

import face_recognition
import cv2
import os
import pickle
from datetime import datetime
import boto3 
from repository.repository import Repository
# from dotenv import load_dotenv
# load_dotenv()
class VideoProcessor:
    def __init__(self, model_path,s3_bucket_name):
        self.model_path = model_path
        self.s3_bucket_name = s3_bucket_name
        self.repository=Repository()
    def process_video_message(self, obj_id, video_content_binary):
        try:
            # Extract id and video blob from the Kafka message
            video_filename = f'temp_video_{obj_id}.mp4'
            with open(video_filename, 'wb') as video_file:
                video_file.write(video_content_binary)

            # Load known faces from the model path
            known_face_encodings, known_face_labels = self.repository.load_known_faces(os.getenv("MODEL"))

            # Process the video using face recognition
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

                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    name = "Unknown"
                    if known_face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = known_face_labels[first_match_index]
                            item = self.repository.get_criminal_records(name)
                            name = item.get("name", name)
                            # records = item.get("criminal_record", [])
                    color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, color, 1)

                video_writer.write(frame)
            video_writer.release()
            with open(videoname, 'rb') as data:
                if os.path.exists(video_filename):
                    self.repository.save_video_to_s3(data, obj_id)

                    os.remove(video_filename)
                    os.remove(videoname)
                    print(f"Sucess saving the video {obj_id} on s3")

        except Exception as e:
            print(f"Error processing video: {e}")



