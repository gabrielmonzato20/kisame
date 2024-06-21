import express from 'express';
import { VideoController } from './controllers/VideoController';

const app = express();
const PORT = process.env.PORT || 3000;
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
  });
app.use(express.json());

app.use('/api', VideoController);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
