from flask import Flask, request, jsonify
from flask_cors import CORS
from service.service import Service
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app, origins=["*"])
service = Service()
@app.route('/process_video', methods=['POST'])
def handle_process_video():
    return service.process_video(request)

@app.route('/process_frame', methods=['POST'])
def handle_process_frame():
    return service.process_frame(request)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT"))