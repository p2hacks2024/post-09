import os
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal
from suggester.spitify_api import get_music_id
from models.activity import Music
from suggester.suggester_models import SuggesterInput, SuggesterOutput
from icecream import ic  # pyright: ignore


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

    emotion: Literal[
        "恐怖", "恥", "悲しみ", "怒り", "嫉妬", "不安", "嫌悪", "孤独感"
    ] = Field(
        description="感情 (e.g. 悲しみ、怒り、嫉妬、不安、恐怖、恥、嫌悪、孤独感)"
        # pattern=r"^[A-Za-z]+$",
    )
    summary: str = Field(
        description="a short summary of happening e.g. 友人との喧嘩, 仕事での失敗, 失恋],"
    )
    music_query: List[str] = Field(  # pyright: ignore
        description="recommended music query based on user prompt",
        min_items=5,
        max_items=5,
    )

    # Custom validator to remove specific unwanted strings
    @field_validator("comment", "summary")
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


class Suggester:
    def __init__(self, input: SuggesterInput):
        self.suggester_input = input

        self.llm = ChatLlamaCpp(  # pyright: ignore
            model_path=get_model_path(),
            n_gpu_layers=-1,
            n_ctx=1024,
            n_batch=512,
            temperature=0.5,
            verbose=True,
        )

        self.question_prompt: PromptTemplate = PromptTemplate(
            input_variables=["statement"],
            template="""
                    あなたは感情分析のエキスパートです。ユーザーが体験した出来事を受けて、
                    以下のタスクを実行してください。
                    また、出来事を2の単語でsummaryを書いてください。
                    次に、出来事に対するコメントを少し長めに敬語で書いてください。このコメントには、
                    ユーザーに対する優しい言葉やアドバイスも含めてください。
                    次に、今のユーザーの心理状態にマッチする曲を検索するために、曲検索のための
                    日本語の単語を1トークンずつ出力してください。
                    最後に、さきほどの曲検索のためのワードの一つをユーザーの感情として出力して
                    ください。
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

        ic(response.music_query)

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

"""            You must always return valid JSON fenced by a markdown 
                    code block. Do not return any additional text."
"""
"""Please analyze the sentiment of the following text and classify it into ONE of the following categories:
                      悲しみ、怒り、嫉妬、不安、恐怖、恥、嫌悪、孤独感. Provide a short explanation of why you classified the text in that way."""
