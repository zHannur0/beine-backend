import tempfile
import urllib
from urllib import request
from moviepy.editor import *


class VideoService:

    def __init__(self):

        pass

    def generate_video(self, audio_urls, images_data):
        audios = []
        images = []
        durations = []
        for audio in audio_urls:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio_file:
                temp_audio_file.write(audio)
                audio_clip = AudioFileClip(temp_audio_file.name)

            audios.append(audio_clip)
            durations.append(audio_clip.duration)

        for image in images_data:
            images.append(ImageClip(image))

        for i in range(5):
            images[i] = images[i].set_duration(durations[i])
            images[i] = images[i].set_audio(audios[i])

        video = concatenate_videoclips([images[0],
                                        images[1],
                                        images[2],
                                        images[3],
                                        images[4]])
        
        return video
