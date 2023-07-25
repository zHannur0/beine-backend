import tempfile
from fastapi import Depends, UploadFile, Response
from typing import List
from pydantic import BaseModel
from ..service import Service, get_service
from . import router
from moviepy.editor import *
from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class GenerateVideoRequest(AppModel):
    prompt: str


@router.post("/newvideo")
def upload_video(
        request: GenerateVideoRequest,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
):
    # user = svc.repository.get_shanyrak(user_id)

    # if user is None:
    #     return Response(status_code=404)

    text = svc.text_service.generate_text(request.prompt)
    image_text = svc.text_service.generate_image_text(text)
    audios = svc.audio_service.text_to_speach(text)
    images = svc.image_service.text_to_image(image_text)
    video = svc.video_service.generate_video(audios, images)
    url = ""
    
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as temp_file:
        video.write_videofile(temp_file.name, fps=10)
        url = svc.s3_service.upload_file(temp_file,
                                         jwt_data.user_id,
                                         temp_file.name)

    svc.repository.add_video(jwt_data.user_id, url)

    # return Response(status_code=200) 
    return {"link": url}