from dataclasses import dataclass

@dataclass
class Music:
    '''
    Spotify APIで取得できる楽曲情報
    '''
    acousticness: float

@dataclass
class Activities:
    '''
    ユーザーのアクティビティ情報
    '''
    timestamp: str
    emotion: str
    weather: str
    temperature: float
    music: Music


