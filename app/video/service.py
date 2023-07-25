from app.config import database

from .repository.repository import VideoRepository
from .adapters.s3_service import S3Service
from .adapters.audio_generating_service import AudioService
from .adapters.image_generating_service import ImageService
from .adapters.text_generating_service import TextService
from .adapters.video_generating_service import VideoService

import os

from dotenv import load_dotenv, dotenv_values

load_dotenv()


class Service:
    def __init__(
            self):
        self.repository = VideoRepository(database)
        self.s3_service = S3Service()
        self.audio_service = AudioService(os.getenv('SOUND_TOKEN'), 
                                          os.getenv('SOUND_USERID'))
        self.image_service = ImageService(os.getenv('TEXT_TO_IMAGE_TOKEN'))
        self.text_service = TextService(os.getenv('OPENAI_API_KEY'))
        self.video_service = VideoService()


def get_service():
    svc = Service()
    return svc
