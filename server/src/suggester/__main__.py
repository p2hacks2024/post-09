from pydantic import BaseModel
from suggester import llm


# I/O
class SuggesterInput(BaseModel):
    """
    Suggesterの入力情報
    """

    emotion: str
    prompt: str
    # activities: List[Activity]


class SuggesterOutput(BaseModel):
    """
    Suggesterの出力情報
    """

    # musics: List[Music]
    situation: str
    comment: str


class Suggester(BaseModel):
    input: SuggesterInput

    def llm_runner(self) -> SuggesterOutput:
        model_path = llm.get_model_path()
        emotion_analyzer = llm.EmotionAnalyzer(model_path=model_path)
        prompt = SuggesterInput.prompt
        result = emotion_analyzer.analyze_emotion(prompt)
        output = SuggesterOutput(situation=result, comment=result)

        return output
