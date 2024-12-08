from dataclasses import dataclass
from typing import List

@dataclass
class Music:
    '''
    Spotify APIで取得できる楽曲情報
    '''
    acousticness: float

@dataclass
class Activity:
    '''
    ユーザーのアクティビティ情報
    '''
    timestamp: str
    emotion: List[float]
    weather: str
    temperature: float
    music: Music