import os
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal
from suggester.spitify_api import get_music_id
from models.activity import Music
from suggester.suggester_models import SuggesterInput, SuggesterOutput


# ファイルパスの取得と設定
def get_model_path() -> str:
    resources_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(resources_dir, "resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf")
    return file_path


# LLMに強制する出力の型
class EmotionAnalysis(BaseModel):
    """
    A result of emotion analysis from user input
    """

    comment: str = Field(
        description="""a comforting comment to user's episode 
        (e.g. What a sad story. I'm so sorry to here that.)""",
    )
    emotion: Literal["lonely", "angry", "envy", "anxious", "fear", "asshamed"] = Field(
        description="emotion (e.g. angry)"
        # pattern=r"^[A-Za-z]+$",
    )
    summary: str = Field(
        description="a short summary of happening e.g. 友人との喧嘩, 仕事での失敗, 失恋],",
        max_length=6,
    )
    music_query: List[str] = Field(  # pyright: ignore
        description="recommended music query based on user prompt",
        min_items=5,
        max_items=5,
    )

    # Custom validator to remove specific unwanted strings
    @field_validator("comment")
    def remove_specific_strings(cls, value: str) -> str:
        # Remove specific characters
        unwanted_strings = ["{", "}", "\n"]
        for unwanted in unwanted_strings:
            value = value.replace(unwanted, "")
        if not value.strip():
            raise ValueError(
                "Comment must contain valid content after removing unwanted characters."
            )
        return value


# モデル設定クラス
class Suggester:
    def __init__(self, input: SuggesterInput):
        self.suggester_input = input

        self.llm = ChatLlamaCpp(  # pyright: ignore
            model_path=get_model_path(),
            n_gpu_layers=-1,
            n_ctx=1024,
            n_batch=512,
            temperature=0.3,
            verbose=True,
        )

        self.question_prompt: PromptTemplate = PromptTemplate(
            input_variables=["statement"],
            template="""
                    あなたは感情分析のエキスパートです。ユーザーが体験した出来事を受けて、
                    以下のタスクを実行してください。
                    また、出来事を一言で、6文字以内でsummaryを書いてください。
                    次に、出来事に対するコメントを少し長めに書いてください。このコメントには、
                    ユーザーに対する慰めも含めてください。
                    次に、ユーザーの出来事に基づいて一つの曲名を書いてください。
                    次に、コメントを元にユーザーの感情を例の中から一つ出力してください。
                    次に、今のユーザーの心理状態に適した曲を検索するために、曲検索のための
                    単語を出力してください
                    以下がユーザーの出来事です。\n
                    {statement}
                """,
        )
        self.structured_llm = self.llm.with_structured_output(EmotionAnalysis)  # pyright: ignore
        self.chain = self.question_prompt | self.structured_llm  # pyright: ignore

    def llm_runner(self) -> SuggesterOutput:
        response: EmotionAnalysis = self.chain.invoke(  # pyright: ignore
            {"statement": self.suggester_input.prompt}
        )
        musics: List[Music] = get_music_id(response.music_query)  # pyright: ignore
        output = SuggesterOutput(
            musics=musics,
            emotion=response.emotion,
            summary=response.summary,
            comment=response.comment,
        )

        return output

    #     return response

    # def analyze_emotion(self, statement: str) -> EmotionAnalysis:
    #     response: EmotionAnalysis = self.chain.invoke({"statement": statement})  # pyright: ignore
    #     return response

    # def get_ids(self, query: str) -> List[Music]:
    #     musics: List[Music] = get_music_id(query)
    #     return musics

    # def get_suggester_output(self, musics: List[Music], ea: EmotionAnalysis) ->SuggesterOutput:
    #     output = SuggesterOutput(musics=musics, summary=ea.summary, comment=ea.comment)
    #     return output


# if __name__ == "__main__":
#     model_path = get_model_path()
#     ea = EmotionAnalyzer()
#     output = ea.llm_runner("上司に怒られてしまった")
#     print(output)
