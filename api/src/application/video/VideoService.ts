import { VideoRepository } from '../../infra/video/VideoRepository';
import { Video } from '../../domain/video/Video';
import { Readable } from 'stream';

export class VideoService {
  private videoRepository: VideoRepository;

  constructor(videoRepository: VideoRepository) {
    this.videoRepository = videoRepository;
  }

  async listVideos(): Promise<Video[]> {
    return this.videoRepository.listVideos();
  }

  async getVideoStream(videoId: string): Promise<Readable> {
    try {
      // Assuming you have a method in VideoRepository to get video stream by ID
      const videoStream = await this.videoRepository.getVideoStream(videoId);
      console.log(videoStream)
      return videoStream;
    } catch (error) {
      console.error('Error getting video stream:', error);
      throw new Error('Internal Server Error');
    }
  }
}
