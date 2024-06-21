import { S3 } from 'aws-sdk';
import { Video } from '../../domain/video/Video';
import { v4 as uuidv4 } from 'uuid';
import dotenv from 'dotenv';

dotenv.config();

export class VideoRepository {
  private s3: S3;

  constructor() {
    this.s3 = new S3({
        endpoint: 'http://localhost:4566', // Change this to match your LocalStack setup
        s3ForcePathStyle: true,
      });
  }

  async listVideos(): Promise<Video[]> {
    const params = {
      Bucket: process.env.S3_BUCKET_NAME!,
    };

    try {
      const data = await this.s3.listObjectsV2(params).promise();
      return data.Contents?.map((item) => ({
        id: uuidv4(),
        title: item.Key!,
        url: `${item.Key!}`,
      })) || [];
    } catch (error) {
      console.error('Error listing videos from S3:', error);
      throw error;
    }
  }
  async getVideoStream(key:string) {

    const params = {
      Bucket: process.env.S3_BUCKET_NAME!,
      Key: key,
    };
    const stream = this.s3.getObject(params).createReadStream();
    return await stream;
  }
}
