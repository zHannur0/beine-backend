from datetime import datetime
from typing import Any, BinaryIO, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult
from typing import Optional


class VideoRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_video(self, user_id: str, title: str, url: str, image_url: str):
        payload = {"user_id": user_id, "title": title, "video_url": url,
                   "image": image_url, "like": [], "dislike": []}

        self.database["beine"].insert_one(payload)

    def all_videos(self):
        return self.database["beine"].find({}).sort([('like', -1)])

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user
    
    def add_like(self, username: str, video_id: str):
        dislikes = self.database["beine"].find_one({'_id': ObjectId(video_id)}).get('dislike', [])
        if username in dislikes:
            self.database["beine"].update_one(
                filter={"_id": ObjectId(video_id)},
                update={
                    "$pull": {
                        "dislike": username,
                    }
                }
            )

        likes = self.database["beine"].find_one({'_id': ObjectId(video_id)}).get('like', [])
        if username in likes:
            return "No"
        
        result = self.database["beine"].update_one(
            filter={"_id": ObjectId(video_id)},
            update={
                "$push": {
                    "like": username,
                }
            }
        )

        return result
    
    def add_dislike(self, username: str, video_id: str):
        likes = self.database["beine"].find_one({'_id': ObjectId(video_id)}).get('like', [])
        if username in likes:
            self.database["beine"].update_one(
                filter={"_id": ObjectId(video_id)},
                update={
                    "$pull": {
                        "like": username,
                    }
                }
            )

        dislikes = self.database["beine"].find_one({'_id': ObjectId(video_id)}).get('dislike', [])
        if username in dislikes:
            return "No"
        
        result = self.database["beine"].update_one(
            filter={"_id": ObjectId(video_id)},
            update={
                "$push": {
                    "dislike": username,
                }
            }
        )

        return result