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
    id: Any = Field(alias="_id")
    username: str
    title: str
    video_url: str
    image: str
    like: List
    dislike: List 


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
        username = svc.repository.get_user_by_id(video["user_id"])["username"]
        res.append(Video(id=video["_id"], username=username, title=video["title"],
                         video_url=video["video_url"],
                         image=video["image"],
                         like=video["like"],
                         dislike=video["dislike"]))
    return GetAllVideosResponse(videos=res)
