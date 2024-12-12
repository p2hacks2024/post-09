# from langchain_community.llms import LlamaCpp
from ast import arg
from tabnanny import verbose
from fastapi import responses
from langchain_community.chat_models import ChatLlamaCpp
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_core.messages.human import HumanMessage
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from models.activity import Music, Activity
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from suggester.spitify_api import get_music_id

# Load the Llama model
llm = ChatLlamaCpp(
    model_path="/home/makebrain/ptwo/post-09/server/src/suggester/resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf",
    n_gpu_layers=-1,
    n_ctx=1024,
    n_batch=512,
    temperature=0.7,
    verbose=True,
)


class EmotionAnalysis(BaseModel):
    """
    A result of emotion analysis from user input
    """

    comment: str = Field(
        description="""a comforting comment to user's episode 
        (e.g. What a sad story. I'm so sorry to here that.)"""
    )
    emotion: str = Field(  # pyright: ignore
        description="emotion (e.g. angry)",
        examples=["sad", "angry", "dissapointed"],
        pattren=r"^[A-Za-z]+$",
    )  # pyright: ignore
    summary: str = Field(
        description="a short summary of happening",
        examples=["友人との喧嘩", "仕事での失敗", "失恋"],
    )
    music_query: str = Field(
        description="recommended music query based on user prompt",
    )


question_prompt = PromptTemplate(
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

structured_llm = llm.with_structured_output(EmotionAnalysis)  # pyright: ignore

chain = question_prompt | structured_llm  # pyright: ignore
response = chain.invoke({"statement": "職場でしこたま怒られてしまった"})  # pyright: ignore

musics = get_music_id(response.music_query)  # pyright: ignore
