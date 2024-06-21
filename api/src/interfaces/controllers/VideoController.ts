import express, { Request, Response } from 'express';
import { VideoService } from '../../application/video/VideoService';
import { VideoRepository } from '../../infra/video/VideoRepository';
import fs from 'fs';

const router = express.Router();
const videoRepository = new VideoRepository();
const videoService = new VideoService(videoRepository);
router.get('/videos', async (_req: Request, res: Response) => {

  try {
    const videos = await videoService.listVideos();
    res.json(videos);
  } catch (error) {
    console.error('Error in VideoController:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/video/:key', async (req, res) => {
try{
        
    const key = req.params.key; // Extract the key from the URL parameter
  

  
    const videoStream = await videoService.getVideoStream(key);

    if (!videoStream) {
      res.status(404).end('Video not found');
      return;
    }

    // Set the appropriate headers for video streaming
    res.setHeader('Content-Type', 'video/mp4');
    res.setHeader('Content-Disposition', 'inline');
    res.setHeader('Content-Disposition', `inline; filename=${key}`);
    videoStream.on('error', (err) => {
        console.error('Error streaming video from S3:', err);
        res.status(500).send('Internal Server Error');
      });
    // Pipe the video stream to the response stream
    videoStream.pipe(res);
  } catch (error) {
    console.error('Error handling video request:', error);
    res.status(500).end('Internal Server Error');
  }
// const videoPath = '/Users/gabrielmonzato/Downloads/test.mp4';
// const stat = fs.statSync(videoPath);
// const fileSize = stat.size;
// const range = req.headers.range;

// if (range) {
//   const parts = range.replace(/bytes=/, '').split('-');
//   const start = parseInt(parts[0], 10);
//   const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;

//   const chunksize = end - start + 1;
//   const file = fs.createReadStream(videoPath, { start, end });
//   const head = {
//     'Content-Range': `bytes ${start}-${end}/${fileSize}`,
//     'Accept-Ranges': 'bytes',
//     'Content-Length': chunksize,
//     'Content-Type': 'video/mp4',
//   };

//   res.writeHead(206, head);
//   file.pipe(res);
// } else {
//   const head = {
//     'Content-Length': fileSize,
//     'Content-Type': 'video/mp4',
//   };

//   res.writeHead(200, head);
//   fs.createReadStream(videoPath).pipe(res);
// }
  });
  

export { router as VideoController };
