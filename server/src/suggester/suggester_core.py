from pydantic import BaseModel

from suggester.suggester_models import SuggesterInput, SuggesterOutput
from models.activity import Activity, Music
from typing import List
from suggester import llm


class Suggester(BaseModel):
    input: SuggesterInput

    def llm_runner(self) -> SuggesterOutput:
        model_path = llm.get_model_path()
        emotion_analyzer = llm.EmotionAnalyzer(model_path=model_path)
        prompt = SuggesterInput.prompt
        response = emotion_analyzer.analyze_emotion(prompt)
        musics = emotion_analyzer.get_ids(response.music_query)
        output = emotion_analyzer.get_suggester_output(musics, response)

        # dummuy output
        # musics = [
        #     Music(name="test1", genre="test_genre1", id="3AoEQRuFf8zVXWqSLo2UOi"),
        #     Music(name="test2", genre="test_genre2", id="4gxEY3Mh5FZZDAJAKPNrCS"),
        # ]
        # output = SuggesterOutput(
        #     musics=musics,
        #     summary="バイトでの失敗",
        #     comment="それはお辛い出来事でしたね。辛い気持ちをflushするために、"
        #     "以下の曲はいかがでしょうか？",
        # )

        return output
