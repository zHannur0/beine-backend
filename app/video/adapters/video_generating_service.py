import base64
import tempfile
import urllib
from urllib import request

from moviepy.editor import *

import io
from PIL import Image
import numpy as np


class VideoService:

    def __init__(self):

        pass

    def generate_video(self, audio_urls, images_data):
        audios = []
        images = []
        durations = []
        for audio in audio_urls:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=True) as temp_file:
                urllib.request.urlretrieve(audio, temp_file.name)
                audio_clip = AudioFileClip(temp_file.name)

            audios.append(audio_clip)
            durations.append(audio_clip.duration)

        for image in images_data:
            image = base64.b64decode(image)
            i = io.BytesIO(image)

            pil_image = Image.open(i)

            # Convert the PIL image to a numpy array
            image_array = np.array(pil_image)

            images.append(ImageClip(image_array))

        for i in range(5):
            images[i] = images[i].set_duration(durations[i])
            images[i] = images[i].set_audio(audios[i])

        video = concatenate_videoclips([images[0],
                                        images[1],
                                        images[2],
                                        images[3],
                                        images[4]])
        
        return video
