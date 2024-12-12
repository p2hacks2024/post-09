from pydantic import BaseModel
from models.activity import Activity, Music
from typing import List


# I/O
class SuggesterInput(BaseModel):
    """
    Suggesterの入力情報
    """

    emotion: str
    prompt: str
    activities: List[Activity]


class SuggesterOutput(BaseModel):
    """
    Suggesterの出力情報
    """

    musics: List[Music]
    summary: str
    comment: str
