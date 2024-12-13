from pydantic import BaseModel
from typing import List


class Music(BaseModel):
    """
    Spotify APIで取得できる楽曲情報
    """

    name: str
    genre: str
    id: str


class Activity(BaseModel):
    """
    ユーザーのアクティビティ情報
    """

    timestamp: str
    emotion: str
    prompt: str
    situation: str
    musics: List[Music]
