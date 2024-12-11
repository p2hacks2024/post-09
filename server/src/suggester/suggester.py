from pydantic import BaseModel

# from suggester import llm
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


class Suggester(BaseModel):
    input: SuggesterInput

    def llm_runner(self) -> SuggesterOutput:
        # model_path = llm.get_model_path()
        # emotion_analyzer = llm.EmotionAnalyzer(model_path=model_path)
        # prompt = SuggesterInput.prompt
        # result = emotion_analyzer.analyze_emotion(prompt)
        # output = SuggesterOutput(situation=result, comment=result)

        # ダミーoutput
        musics = [
            Music(name="test1", genre="test_genre1", id="3AoEQRuFf8zVXWqSLo2UOi"),
            Music(name="test2", genre="test_genre2", id="4gxEY3Mh5FZZDAJAKPNrCS"),
        ]
        output = SuggesterOutput(
            musics=musics,
            summary="バイトでの失敗",
            comment="それはお辛い出来事でしたね。辛い気持ちをflushするために、"
            "以下の曲はいかがでしょうか？",
        )

        return output
