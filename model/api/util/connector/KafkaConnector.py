from kafka import KafkaProducer
import uuid
import json
import base64
class KafkaConnector:
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            max_request_size=100 * 1024 * 1024
        )
        self.topic = topic


    def on_send_success(self,record_metadata):
        print("Message sent to Kafka. Topic:", record_metadata.topic, "Partition:", record_metadata.partition, "Offset:", record_metadata.offset)

    def on_send_error(self,excp):
        print("Failed to send message to Kafka:", excp)
    
    def send_video_object(self, video_data):
        video_id = str(uuid.uuid4())
        chunk_size =1024  # 1 MB chunk size (you can adjust this value)
        try:
            while True:
                chunk = video_data.read(chunk_size)
                if not chunk:
                    break

                video_object = {"id": video_id, "chunk": base64.b64encode(chunk).decode('utf-8')}
                self.producer.send(self.topic, value=video_object).add_callback(self.on_send_success).add_errback(self.on_send_error)
                self.producer.flush()

            # Signal the end of video transmission by sending an empty chunk
            self.producer.send(self.topic, value={"id": video_id, "chunk": ""}).add_callback(self.on_send_success).add_errback(self.on_send_error)
            self.producer.flush()

            return video_id

        except Exception as e:
            print(f"Error sending video chunks: {e}")