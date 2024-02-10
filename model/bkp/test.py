import os 
import pickle
def load_known_faces(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data['encodings'], data['labels']

known_faces_file = 'known_faces.pkl'
if os.path.exists(known_faces_file):
    known_face_encodings, known_face_labels = load_known_faces(known_faces_file)
    print(f"size2:{len(known_face_encodings)} , {len(known_face_labels)}")
