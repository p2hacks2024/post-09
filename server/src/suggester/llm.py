from ast import get_source_segment
import os
import re
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from suggester.spitify_api import get_music_id
from models.activity import Music
from suggester.suggester_models import SuggesterOutput


# LLMに強制する出力の型
class EmotionAnalysis(BaseModel):
    """
    A result of emotion analysis from user input
    """

    comment: str = Field(  # pyright: ignore
        description="""a comforting comment to user's episode 
        (e.g. What a sad story. I'm so sorry to here that.)"""
    )
    emotion: str = Field(  # pyright: ignore
        description="emotion (e.g. angry)",
        examples=["sad", "angry", "dissapointed"],
        pattren=r"^[A-Za-z]+$",
    )  # pyright: ignore
    summary: str = Field(  # pyright: ignore
        description="a short summary of happening",
        examples=["友人との喧嘩", "仕事での失敗", "失恋"],
    )
    music_query: str = Field(  # pyright: ignore
        description="recommended music query based on user prompt",
    )


# モデル設定クラス
class EmotionAnalyzer(BaseModel):
    model_path: str  # model_pathはpydanticのフィールドとして定義
    llm: ChatLlamaCpp = None  # llmフィールドを定義
    question_prompt: PromptTemplate = None  # PromptTemplateフィールドを定義
    structured_llm: ChatLlamaCpp = None  # structured_llmフィールドを定義
    chain: str = None  # chainフィールドを定義（型は適切に設定）

    def __init__(self, **kwargs):  # pyright: ignore
        super().__init__(**kwargs)
        self.llm = ChatLlamaCpp(  # pyright: ignore
            model_path=self.model_path,
            n_gpu_layers=-1,
            n_ctx=1024,
            n_batch=512,
            temperature=0.7,
            verbose=True,
        )

        self.question_prompt: PromptTemplate = PromptTemplate(
            input_variables=["statement"],
            template="""
                    あなたは感情分析のエキスパートです。ユーザーが体験した出来事を受けて、
                    以下のタスクを実行してください。
                    また、出来事をとても短く要約してください。
                    次に、出来事に対するコメントを少し長めに書いてください。このコメントには、
                    ユーザーに対する慰めも含めてください。
                    次に、ユーザーの出来事に基づいて一つの曲名を書いてください。
                    次に、コメントを元にユーザーの感情を例の中から一つ選んで出力してください。
                    (例： lonely, angry, complicated, envy, anxious, fear, asshamed)
                    次に、今のユーザーの心理状態に適した曲を検索するために、曲検索のための
                    単語を出力してください
                    Don't include any symbols.
                    以下がユーザーの出来事です。
                    {statement}
                """,
        )
        self.structured_llm = self.llm.with_structured_output(EmotionAnalysis)  # pyright: ignore
        self.chain = self.question_prompt | self.structured_llm  # pyright: ignore

    def analyze_emotion(self, statement: str) -> EmotionAnalysis:
        response: EmotionAnalysis = self.chain.invoke({"statement": statement})  # pyright: ignore
        return response

    def get_ids(self, query: str) -> List[Music]:
        musics: List[Music] = get_music_id(query)
        return musics

    def get_suggester_output(self, musics: List[Music], ea: EmotionAnalysis):
        output = SuggesterOutput(musics=musics, summary=ea.summary, comment=ea.comment)
        return output


# ファイルパスの取得と設定
def get_model_path() -> str:
    resources_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(resources_dir, "resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf")
    return file_path


if __name__ == "__main__":
    model_path = get_model_path()
    ea = EmotionAnalyzer(model_path=model_path)

    statement = "テストで100点を取ったが、父親が褒めてくれなかった"
    response = ea.analyze_emotion(statement)
    musics = ea.get_ids(response.music_query)
    output = ea.get_suggester_output(musics, response)
    print(output)
