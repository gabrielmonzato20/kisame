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
load_dotenv()

class FrameProcessor:
    def __init__(self):
        self.repository = Repository()
    def process(self, frame_data):
        known_face_encodings, known_face_labels = self.repository.load_known_faces(os.getenv("MODEL"))

        image_bytes = base64.b64decode(frame_data)
        image_stream = BytesIO(image_bytes)
        image = Image.open(image_stream)
        frame_np = np.array(image, dtype=np.uint8)

        if frame_np is None or frame_np.size == 0:
            return {'error': 'Invalid image data'}

        face_locations = face_recognition.face_locations(frame_np)
        face_encodings = face_recognition.face_encodings(frame_np, face_locations)

        result = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            records = []
            if known_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                if True in matches:
                    
                    first_match_index = matches.index(True)
                    name = known_face_labels[first_match_index]
                    item = self.repository.get_criminal_records(name)
                    name = item.get("name", name)
                    records = item.get("criminal_record", [])

            result.append({'name': name, 'box': {'top': top, 'right': right, 'bottom': bottom, 'left': left},
                           "records": records})

        return result
