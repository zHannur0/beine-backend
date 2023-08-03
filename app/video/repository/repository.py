from datetime import datetime
from typing import Any, BinaryIO, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult


class VideoRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_video(self, user_id: str, title: str, url: str):
        payload = {"user_id": user_id, "title": title, "video_url": url}

        self.database["beine"].insert_one(payload)

    def all_videos(self):
        return self.database["beine"].find({})
