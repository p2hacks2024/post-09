from pydantic import BaseModel
from typing import List


class Music(BaseModel):
    """
    Spotify APIで取得できる楽曲情報
    """

    track_name: str
    track_id: str
    album_id: str
    popularity: int


class Activity(BaseModel):
    """
    ユーザーのアクティビティ情報
    """

    timestamp: str
    emotion: str
    prompt: str
    situation: str
    musics: List[Music]
