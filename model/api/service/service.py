from application.FrameProcessor import  FrameProcessor
from application.VideoProcessor import VideoProcessor
from flask import jsonify

class Service:
    def __init__(self):
        pass

    def process_video(self,request):
        video_file = request.files['video']
        application = VideoProcessor()
        result = application.process(video_file)
        return jsonify(result)

    def process_frame(self,request):
        data = request.get_json()

        if not data or 'frameData' not in data:
            return jsonify({'error': 'Missing or invalid frameData parameter'})

        frame_data = data['frameData']

        try:
            application = FrameProcessor()
            result = application.process(frame_data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': f'Error processing frame: {str(e)}'})

