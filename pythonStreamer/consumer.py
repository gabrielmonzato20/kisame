import json
import base64
from kafka import KafkaConsumer, OffsetAndMetadata
from video_processor import VideoProcessor
import os

class VideoServer:
    def __init__(self, kafka_bootstrap_servers, kafka_topic, model_path, s3_bucket_name, kafka_group_id):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic = kafka_topic
        self.model_path = model_path
        self.consumer = None
        self.video_processor = None
        self.s3_bucket_name = s3_bucket_name
        self.kafka_group_id = kafka_group_id
        self.video_chunks = {}

    def start(self):
        consumer_conf = {
            'bootstrap_servers': self.kafka_bootstrap_servers,
            'auto_offset_reset': 'earliest',
            'group_id': self.kafka_group_id,
        }

        self.consumer = KafkaConsumer(self.kafka_topic, **consumer_conf, value_deserializer=lambda x: json.loads(x))
        self.video_processor = VideoProcessor(self.model_path, self.s3_bucket_name)

        try:
            while True:
                # print("Searching...")
                messages = self.consumer.poll(timeout_ms=1000)
                if not messages:
                    # No messages found, continue to the next iteration
                    print("no message")
                    continue

                # Process the messages
                for partition, message_list in messages.items():
                    print("Processing...")

                    for msg in message_list:
                        if msg.value is None:
                            # Skip messages with no value
                            continue

                        try:

                            data = msg.value

                            obj_id = data['id']
                            video_content_base64 = data['chunk']

                            # Decode base64 to binary
                            video_content_binary = base64.b64decode(video_content_base64)

                            # Check for an empty chunk to stop processing
                            if not video_content_binary:
                                print(f"Received empty chunk. Stopping processing for video {obj_id}")

                                # Concatenate all chunks
                                full_video_binary = b''.join(self.video_chunks.get(obj_id, []))
                                # Process the full video
                                self.process_full_video(obj_id, full_video_binary)

                                # Clear the chunks for this video
                                self.video_chunks.pop(obj_id, None)

                                # Continue to the next iteration
                                continue

                            # Append the chunk to the list
                            self.video_chunks.setdefault(obj_id, []).append(video_content_binary)

                        except Exception as e:
                            print(f"Error processing message: {e}")

                    # Commit the offsets to mark messages as processed for this partition
                    offsets_to_commit = {partition: OffsetAndMetadata(msg.offset + 1, None) for msg in message_list}
                    self.consumer.commit(offsets=offsets_to_commit)

        except KeyboardInterrupt:
            pass

        finally:
            self.cleanup()

    def process_full_video(self, obj_id, full_video_binary):
        try:
            video_processor = VideoProcessor(self.model_path, self.s3_bucket_name)
            video_processor.process_video_message(obj_id, full_video_binary)



        except Exception as e:
            print(f"Error processing full video: {e}")

    def cleanup(self):
        if self.consumer:
            self.consumer.close()
if __name__ == '__main__':
    kafka_bootstrap_servers = os.getenv("KAFKA_SERVER")
    kafka_topic = os.getenv("KAFKA_TOPIC")
    model_path = os.getenv("MODEL")  # Make sure to set the MODEL environment variable
    bucket_name = os.getenv("S3_BUCKET_NAME")
    kafka_group_id = os.getenv("KAFKA_GROUP_ID")
    video_server = VideoServer(kafka_bootstrap_servers, kafka_topic, model_path,bucket_name,kafka_group_id)
    video_server.start()