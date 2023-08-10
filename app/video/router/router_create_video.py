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
import json


class GenerateVideoRequest(AppModel):
    prompt: str
    lang: str

@router.post("/newvideo")
def upload_video(
        request: GenerateVideoRequest,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
):
    # user = svc.repository.get_shanyrak(user_id)

    # if user is None:
    #     return Response(status_code=404)
    pr = request.prompt
    if request.lang == 'Қазақ':
        pr = svc.text_service.translate_prompt(request.prompt)

    if pr == "NO":
         return Response(status_code=404)

    text = svc.text_service.generate_text(pr)
    lang = ""

    try:
        json.loads(text)
    except:
        return Response(status_code=404)

    if request.lang == 'Қазақ':
         text_json = svc.text_service.translate(text)
         lang = "kk-KZ"
         if text_json == "NO":
              return Response(status_code=404) 
    else:
         text_json = json.loads(text)
         lang = "en-US"
   

    image_text = svc.text_service.generate_image_text(text)

    try:
        json.loads(image_text)
    except:
        return Response(status_code=404)
    
    
    audios = svc.audio_service.text_to_speach(text_json,lang)
    images = svc.image_service.text_to_image(image_text)
    video = svc.video_service.generate_video(audios, images)
    url = ""
    image_url = ""
    image = svc.image_service.convert_url_to_image(images[0])


    print(text)
    print(image_text)
    
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as temp_file:
        video.write_videofile(temp_file.name, fps=10)
        url = svc.s3_service.upload_file(temp_file,
                                         jwt_data.user_id,
                                         temp_file.name)
        
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp_file:
            image.save(tmp_file.name)
            image_url = svc.s3_service.upload_file(tmp_file, 
                                                   jwt_data.user_id,
                                                   tmp_file.name)

    svc.repository.add_video(jwt_data.user_id, request.prompt.capitalize(), url, image_url)

    # return Response(status_code=200) 
    return {"link": url}