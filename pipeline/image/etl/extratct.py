import face_recognition
import os
import boto3
import cv2
import uuid

os.environ['AWS_ACCESS_KEY_ID'] = 'your-localstack-access-key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-localstack-secret-key'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # Update with the desired region

# Set the LocalStack endpoint URL
localstack_endpoint_url = 'http://localhost:4566'  # Update with the correct LocalStack endpoint

s3 = boto3.client("s3", endpoint_url=localstack_endpoint_url)
dynamodb = boto3.resource("dynamodb", endpoint_url=localstack_endpoint_url)

# Create DynamoDB table if not exists
table_name = "gabrielmonzatorecord"
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
    # Wait until the table is created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

except dynamodb.meta.client.exceptions.ResourceInUseException:
    # Table already exists
    table = dynamodb.Table(table_name)

dataset_path = '/Users/gabrielmonzato/Documents/kisame/model/data/lfw/lfw-deepfunneled/lfw-deepfunneled'
bucket_name = 'gabrielmonzatorawimage12321'

labels = os.listdir(dataset_path)

for label in labels:
    label_path = os.path.join(dataset_path, label)
    if os.path.isdir(label_path):
        for image_name in os.listdir(label_path):
            image_path = os.path.join(label_path, image_name)
            if image_name.endswith('.jpg') or image_name.endswith('.png'):
                try:
                    img = face_recognition.load_image_file(image_path)
                    face_locations = face_recognition.face_locations(img)
                    if face_locations:
                        top, right, bottom, left = face_locations[0]
                        face_image = img[top:bottom, left:right]
                        unique_key = str(uuid.uuid4())
                        output_image_path = f"tmp/{unique_key}.jpeg"
                        print(f"Saving image {label} into S3 bucket with key: {unique_key}")
                        cv2.imwrite(output_image_path, cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))

                        # # Upload the image to the S3 bucket
                        # s3.upload_file(output_image_path, bucket_name, unique_key)
                        # # Remove the temporary local file
                        # print(f"Removing image {label} from temp dir: {unique_key}")
                        # os.remove(output_image_path)
                        # print("Saving the record on the DynamoDB table")
                        # table.put_item(
                        #     Item={
                        #         'id': unique_key,
                        #         'name': label,
                        #         'criminal_record': []
                        #     }
                        # )
                except Exception as e:
                    print(f"Error processing image {image_path}: {str(e)}")
