from typing import Any, List

from fastapi import Depends, Response, UploadFile
from moviepy.editor import *
from pydantic import BaseModel, Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


@router.post("/{video_id: str}/like")
def add_like(
    video_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    username = svc.repository.get_user_by_id(jwt_data.user_id)["username"]

    res = svc.repository.add_like(username, video_id)

    if res == "No":
        return Response(status_code=404)

    return Response(status_code=200)
