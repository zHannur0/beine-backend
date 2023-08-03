from typing import Any, List

from fastapi import Depends, Response, UploadFile
from moviepy.editor import *
from pydantic import BaseModel, Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Video(AppModel):
    title: str
    video_url: str
    image: str


class GetAllVideosResponse(AppModel):
    videos: List[Video]


@router.get("/allvideos", response_model=GetAllVideosResponse)
def get_videos(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    res = []
    videos = svc.repository.all_videos()
    for video in videos:
        res.append(Video(**video))
    return GetAllVideosResponse(videos=res)
