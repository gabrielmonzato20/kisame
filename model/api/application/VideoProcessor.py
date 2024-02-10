import cv2
import face_recognition
from datetime import datetime
import uuid
from PIL import Image
import base64
from io import BytesIO
import numpy as np
from repository.repository import Repository
from dotenv import load_dotenv
import os 
from util.connector.KafkaConnector import KafkaConnector
load_dotenv()

class VideoProcessor:
    def __init__(self):
        self.repository = Repository()
        self.kafka = KafkaConnector(os.getenv("KAFKA_SERVER"),os.getenv("KAFKA_TOPIC"))

    def process(self, video_file):
        # known_face_encodings, known_face_labels = self.repository.load_known_faces(os.getenv("MODEL"))
        video_id=self.kafka.send_video_object(video_file)
        # video_filename = 'temp_video.mp4'
        # video_file.save(video_filename)

        # video_capture = cv2.VideoCapture(video_filename)

        # frame_width = int(video_capture.get(3))
        # frame_height = int(video_capture.get(4))

        # timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # videoname = f'video_{timestamp}.mp4'
        # video_writer = cv2.VideoWriter(videoname, cv2.VideoWriter_fourcc(*'avc1'), 30, (frame_width, frame_height))

        # while True:
        #     ret, frame = video_capture.read()
        #     if not ret:
        #         break

        #     face_locations = face_recognition.face_locations(frame)
        #     face_encodings = face_recognition.face_encodings(frame, face_locations)

        #     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #         name = "Unknown"
        #         if known_face_encodings:
        #             matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        #             if True in matches:
        #                 first_match_index = matches.index(True)
        #                 name = known_face_labels[first_match_index]
        #                 item = self.repository.get_criminal_records(name)
        #                 name = item.get("name", name)
        #                 records = item.get("criminal_record", [])
        #         color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        #         cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        #         font = cv2.FONT_HERSHEY_DUPLEX
        #         cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, color, 1)

        #     video_writer.write(frame)

        # video_writer.release()
        # unique_key = str(uuid.uuid4())
        # with open(videoname, 'rb') as data:
        #     self.repository.save_video_to_s3(data, unique_key)
        #     os.remove(videoname)
        #     os.remove(video_filename)
            
        return {'message': f'Video {video_id} processed and saved successfully'}
